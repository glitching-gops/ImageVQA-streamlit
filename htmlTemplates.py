# htmlTemplates.py

css = '''
<style>
    /* Global styles */
    body {
        background-color: #121212 !important;
        color: #ffffff !important;
    }

    /* Override Streamlit's default background */
    .stApp {
        background-color: #121212 !important;
    }




    /* Main container styling */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
        background: #121212;
        min-height: 100vh;
    }

    /* Message container styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: flex-start;
        position: relative;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
    }

    .chat-message:hover {
        transform: translateY(-2px);
    }

    /* User message styling */
    .human-message {
        background: #1e1e1e;
        margin-left: 50px;
        border-bottom-left-radius: 0.5rem;
        border-left: 3px solid #7289da;
    }

    /* Bot message styling */
    .ai-message {
        background: #2d2d2d;
        margin-right: 50px;
        border-bottom-right-radius: 0.5rem;
        border-right: 3px solid #00b4d8;
    }

    /* Avatar styling */
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        position: absolute;
        transition: transform 0.3s ease;
    }

    .avatar:hover {
        transform: scale(1.1);
    }

    .ai-message .avatar {
        background: #00b4d8;
        padding: 5px;
        left: auto;
        right: -50px;
        box-shadow: 0 2px 4px rgba(0,180,216,0.3);
    }

    .human-message .avatar {
        background: #7289da;
        padding: 5px;
        left: -50px;
        box-shadow: 0 2px 4px rgba(114,137,218,0.3);
    }

    /* Message content styling */
    .message-content {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
        color: #ffffff;
        font-size: 1.1rem;
        line-height: 1.5;
    }

    /* Timestamp styling */
    .message-timestamp {
        font-size: 0.85rem;
        color: #888888;
        align-self: flex-end;
        font-style: italic;
    }

    /* Code block styling */
    .message-content pre {
        background: #2b2b2b;
        color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        overflow-x: auto;
        font-family: 'Fira Code', 'Courier New', monospace;
        border: 1px solid #3d3d3d;
    }

    /* Input area styling */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1.5rem;
        background: rgba(18, 18, 18, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 0 -4px 10px rgba(0,0,0,0.3);
        border-top: 1px solid #2d2d2d;
    }

    /* Sidebar styling */
    .sidebar {
        background: #1e1e1e;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    .sidebar h3 {
        margin-top: 0;
        margin-bottom: 1.2rem;
        color: #ffffff;
        font-size: 1.2rem;
        border-bottom: 2px solid #00b4d8;
        padding-bottom: 0.5rem;
    }

    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        margin-top: 0.8rem;
        background: linear-gradient(145deg, #006e85, #005977);
        color: white;
        border: none;
        padding: 0.8rem;
        font-weight: 600;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,180,216,0.3);
    }

    /* File uploader styling */
    .uploadedFile {
        border: 2px solid #2d2d2d;
        border-radius: 0.5rem;
        padding: 1.2rem;
        margin-top: 1.2rem;
        background: rgba(255,255,255,0.05);
    }

    /* Slider styling */
    .stSlider {
        padding: 1.2rem 0;
    }


    /* Select box styling */
    .stSelectbox {
        margin-bottom: 1.2rem;
    }

    .stSelectbox > div > div {
        background-color: #1e1e1e;
        border-color: #2d2d2d;
        color: white;
    }

    /* Loading spinner styling */
    .stSpinner {
        text-align: center;
        padding: 2rem;
        color: #00b4d8;
    }

    /* Error message styling */
    .stError {
        background: rgba(255,69,58,0.1);
        border-left: 5px solid #ff453a;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        color: #ff453a;
    }

    /* Success message styling */
    .stSuccess {
        background: rgba(48,209,88,0.1);
        border-left: 5px solid #30d158;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        color: #30d158;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #121212;
    }

    ::-webkit-scrollbar-thumb {
        background: #00b4d8;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #0096c7;
    }

    /* Override streamlit elements */
    .st-emotion-cache-1gulkj5,
    .st-emotion-cache-1y4p8pa {
        background-color: #121212 !important;
    }

    .st-emotion-cache-1v0mbdj > img {
        background-color: transparent;
    }
</style>
'''

# Template for user messages
user_template = '''
<div class="chat-message human-message">
    <img class="avatar" src="https://api.dicebear.com/7.x/avataaars/svg?seed=user" alt="Human"/>
    <div class="message-content">
        {{MSG}}
        <div class="message-timestamp">{{TIME}}</div>
    </div>
</div>
'''

# Template for bot messages
bot_template = '''
<div class="chat-message ai-message">
    <img class="avatar" src="https://api.dicebear.com/7.x/bottts/svg?seed=bot" alt="AI"/>
    <div class="message-content">
        {{MSG}}
        <div class="message-timestamp">{{TIME}}</div>
    </div>
</div>
'''

