import os
import time
import logging
from typing import Dict
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
import base64
from PIL import Image
import shutil
from pathlib import Path
from htmlTemplates import bot_template, user_template, css
from groq import Groq

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Constants
TEMP_DIR = Path('.temp')
MODEL = "llama-3.2-90b-vision-preview"

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def encode_image(image_path: str) -> str:
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding image: {e}")
        raise

def get_conversation_chain(image_path: str, temperature: float):
    """Creates a conversational chain using Groq API"""
    base64_image = encode_image(image_path)
    messages = []
    
    def custom_conversation_chain(input_dict: Dict) -> Dict:
        try:
            # Prepare the message with image and question
            current_messages = messages.copy()
            current_messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": input_dict['question']
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            })
            
            # Make API call to Groq
            chat_completion = client.chat.completions.create(
                messages=current_messages,
                model=MODEL,
                temperature=temperature
            )
            
            answer = chat_completion.choices[0].message.content
            
            # Store messages for chat history
            messages.append({
                "role": "user",
                "content": input_dict['question']
            })
            messages.append({
                "role": "assistant",
                "content": answer
            })
            
            return {
                'answer': answer,
                'chat_history': messages
            }
        except Exception as e:
            logger.error(f"Error in conversation chain: {e}")
            raise

    return custom_conversation_chain, messages

def initialize_session_state():
    """Initialize all session state variables"""
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None
    if "image_path" not in st.session_state:
        st.session_state.image_path = None
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    if "process_question" not in st.session_state:
        st.session_state.process_question = False

def format_timestamp(timestamp):
    """Format timestamp for display"""
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

def handle_submit():
    st.session_state.process_question = True

def main():
    st.set_page_config(page_title='Chat with your image', layout='wide')
    st.write(css, unsafe_allow_html=True)
    
    initialize_session_state()

    # Sidebar configuration
    with st.sidebar:
        st.subheader("Configuration")
        
        # Temperature control
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            key="temperature",
            help="Higher values make the output more random, lower values make it more focused"
        )
        
        st.subheader("Upload Image")
        uploaded_image = st.file_uploader("Choose your image and Press OK", type=["jpg", "jpeg", "png"])

        if uploaded_image is not None:
            st.session_state.uploaded_image = uploaded_image
            preview_image = Image.open(uploaded_image)
            st.image(preview_image, caption='Uploaded Image', use_container_width=True)

        if st.button("Process Image") and st.session_state.uploaded_image is not None:
            with st.spinner("Processing your image..."):
                try:
                    # Save the uploaded image temporarily
                    temp_path = TEMP_DIR / f"temp_image_{int(time.time())}.jpg"
                    TEMP_DIR.mkdir(exist_ok=True)
                    
                    with open(temp_path, "wb") as f:
                        f.write(st.session_state.uploaded_image.getbuffer())

                    # Generate conversation chain
                    st.session_state.conversation, st.session_state.chat_history = get_conversation_chain(
                        str(temp_path),
                        temperature
                    )
                    st.session_state.image_path = temp_path

                    st.success("Image processed successfully!")
                except Exception as e:
                    st.error(f"Error processing image: {e}")
                    logger.error(f"Error processing image: {e}")

    # Main chat interface
    st.title('Chat with your image')
    
    # Display chat history
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            timestamp = format_timestamp(time.time())
            if message["role"] == "user":
                formatted_message = user_template.replace("{{MSG}}", message["content"]).replace("{{TIME}}", timestamp)
            else:
                formatted_message = bot_template.replace("{{MSG}}", message["content"]).replace("{{TIME}}", timestamp)
            st.write(formatted_message, unsafe_allow_html=True)

    # Question input form
    with st.form(key='question_form', clear_on_submit=True):
        user_question = st.text_input("Ask a question about the image:", key="question")
        submitted = st.form_submit_button("Enter", on_click=handle_submit)

    # Process the question outside the callback
    if st.session_state.process_question and user_question and st.session_state.conversation:
        try:
            with st.spinner("Thinking..."):
                response = st.session_state.conversation({'question': user_question})
                st.session_state.chat_history = response['chat_history']
                st.session_state.process_question = False
                st.rerun()
        except Exception as e:
            st.error(f"Error processing question: {e}")
            logger.error(f"Error processing question: {e}")
            st.session_state.process_question = False

if __name__ == '__main__':
    try:
        main()
    finally:
        # Cleanup temporary files
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)