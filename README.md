# ImageVQA Streamlit App

A Visual Question Answering (VQA) application specialized in analyzing complex diagrams, flowcharts, and graphs. Built with Streamlit and powered by Llama 3.2 Vision (90B) through Groq's inference API, this app enables users to have interactive conversations about technical visual content.

🚀 **Try the live demo**: [https://image-v-q-a-app-omit.streamlit.app/](https://image-v-q-a-app-omit.streamlit.app/)

## Model Details

The application uses Llama 3.2 Vision (90B parameter model), which excels at:
- Processing and understanding complex diagrams and technical visualizations
- Handling detailed visual-language tasks with high accuracy
- Providing comprehensive natural language responses about technical content
- Real-time inference through Groq's high-performance API

## Installation

```bash
# Clone the repository
git clone https://github.com/glitching-gops/ImageVQA-streamlit.git
cd ImageVQA-streamlit

# Install required dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your Groq API key to .env file
```

### Key Dependencies
- `streamlit`: Web application framework
- `groq`: Client for Groq's inference API
- `Pillow`: Image processing
- `python-dotenv`: Environment variable management

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Configure the model:
   - Adjust the temperature slider (0.0-2.0) for response variability
   - Higher values (>1.0) increase creativity
   - Lower values (<1.0) increase focus and precision

3. Upload an image:
   - Click "Choose your image" in the sidebar
   - Support for JPG, JPEG, and PNG formats
   - Click "Process Image" to initialize

4. Ask questions about your diagram/image in the chat interface

## Project Structure
```
ImageVQA-streamlit/
├── main.py              # Main application file
├── htmlTemplates.py     # HTML templates for chat interface
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables
└── .temp/              # Temporary image storage
```

## Acknowledgments

- **Groq** for providing lightning-fast, open-source inference capabilities
- **Meta** for Llama 3.2 Vision model, pushing boundaries in vision-language understanding
- **Streamlit** team for their excellent web application framework


## Contact

Created by [@glitching-gops](https://github.com/glitching-gops)

Project Link: [https://github.com/glitching-gops/ImageVQA-streamlit](https://github.com/glitching-gops/ImageVQA-streamlit)