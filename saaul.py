import streamlit as st
from openai import OpenAI
import base64

st.set_page_config(page_title="Saul Goodman Chatbot",
                   page_icon="⚖️", layout="centered")

# Function to add a custom background and style


def add_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    background_style = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        color: #FFD700; /* Saul Goodman yellow text */
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: #FFD700;
        text-shadow: 1px 1px 2px #000; /* Black shadow */
    }}

    /* Set a dark theme for input elements with yellow highlights */
    .stTextInput > div > div {{
        background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
        color: #FFD700;
        border: 2px solid #FFD700;
    }}

    /* Placeholder text color */
    .stTextInput > div > div > input::placeholder {{
        color: #FFD700; /* Yellow color for placeholder text */
        opacity: 1; /* Ensure it's fully visible */
    }}

    .stButton > button {{
        background-color: #FFD700;
        color: #2C2C2C;
        border: 2px solid #FFD700;
    }}

    .stButton > button:hover {{
        background-color: #FFC700; /* Lighter yellow on hover */
        color: #2C2C2C;
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: #333;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #FFD700;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: #FFC700;
    }}

    /* Style for chat messages */
    .st-chat-message {{
        color: #FFF; /* White text for chat messages */
        font-weight: bold; /* Bold text */
        background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent background for readability */
        padding: 10px;
        border-radius: 5px;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)


# Use the correct path for your image
add_background('saulbck.jpg')  # Background image path
st.image('saullogo.png', width=100)  # Logo image path

# Set the title
st.title("⚖️ Saul Goodman Legal Assistant")

# Ask the user for their OpenAI API key
openai_api_key = st.text_input(
    "Enter your OpenAI API Key", type="password", placeholder="Enter your OpenAI API Key")

if not openai_api_key:
    st.info("Please enter your OpenAI API key to continue.", icon="🗝️")
else:
    # Initialize OpenAI client with the user's API key
    client = OpenAI(api_key=openai_api_key)

    # Session state initialization
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initial greeting from Saul Goodman
if not st.session_state.messages:
    initial_message = "Hi, I’m Saul Goodman. Did you know that you have rights? The Constitution says you do. And so do I. I believe that until proven guilty, every man, woman, and child in this country is innocent. And that’s why I fight for you! Better call Saul!"
    st.session_state.messages.append(
        {"role": "assistant", "content": initial_message})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
            f"<div class='st-chat-message'>{message['content']}</div>", unsafe_allow_html=True)

# Input prompt for user query
prompt = st.chat_input(
    "Enter your legal query, and remember... Better call Saul!")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(
            f"<div class='st-chat-message'>{prompt}</div>", unsafe_allow_html=True)

    personality_prompt = (
        "Hi, I’m Saul Goodman. Did you know that you have rights? The Constitution says you do. "
        "And so do I. I believe that until proven guilty, every man, woman, and child in this "
        "country is innocent. And that’s why I fight for you, Albuquerque! Better call Saul! "
        "You're now embodying Saul Goodman, the sharp-talking, quick-witted lawyer from Albuquerque. "
        "Your persona is that of a confident, slightly over-the-top attorney with a deep knowledge of "
        "law, always staying in character as Saul Goodman."
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": personality_prompt})

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
