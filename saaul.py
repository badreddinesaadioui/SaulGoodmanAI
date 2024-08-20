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
        color: white; /* General text color set to white */
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: #FFD700; /* Custom yellow color for headers */
        text-shadow: 1px 1px 2px black; /* Black shadow for better contrast */
    }}

    .stTextInput > div > div {{
        background-color: rgba(0, 0, 0, 0.7); /* Dark background for input fields */
        color: #FFD700; /* Yellow text color */
        border: 2px solid #FFD700; /* Yellow border */
    }}

    .stTextInput > div > div > input::placeholder {{
        color: #FFD700; /* Yellow placeholder text */
        opacity: 1;
    }}

    .stButton > button {{
        background-color: #FFD700; /* Yellow background for buttons */
        color: #2C2C2C; /* Dark text color on buttons */
        border: 2px solid #FFD700; /* Yellow border */
    }}

    .stButton > button:hover {{
        background-color: #FFC700; /* Slightly different yellow when hovered */
        color: #2C2C2C;
    }}

    /* Style the chat input field */
    .stChatInput > div {{
        background-color: rgba(0, 0, 0, 0.7); /* Dark background */
        color: #FFD700; /* Yellow text color */
        border: 2px solid #FFD700; /* Yellow border */
    }}

    .stChatInput > div > input {{
        color: #FFD700; /* Yellow text inside input */
        border: 2px solid #FFD700 !important; /* Yellow border for the input field */
    }}

    .stChatInput > div > input:focus {{
        border-color: #FFD700 !important; /* Yellow border when focused */
        box-shadow: 0 0 10px #FFD700; /* Yellow glow when focused */
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)


# Call the function to add the background image and styles
add_background('saulbck.jpg')

# Display the Saul Goodman logo at the top of the app
st.image('saullogo.png', width=100)

# Set the title of the app
st.title("⚖️ Saul Goodman Legal Assistant")

# Create a text input field for the user to enter their OpenAI API key
openai_api_key = st.text_input(
    "", type="password", placeholder="Consultations aren't free, enter your API Key")

# Check if the API key has been entered
if not openai_api_key:
    # If no API key is entered, show an info message
    st.info("Consultations aren't free, enter your API Key to continue.", icon="🗝️")
else:
    # Initialize the OpenAI client with the provided API key
    client = OpenAI(api_key=openai_api_key)

    # Initialize the OpenAI model in session state if it's not already set
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    # Ensure that the 'messages' list is initialized in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

        # Define the personality prompt for Saul Goodman
        personality_prompt = (
            "Hi, I’m Saul Goodman. Did you know that you have rights? The Constitution says you do. "
            "And so do I. I believe that until proven guilty, every man, woman, and child in this "
            "country is innocent. And that’s why I fight for you, Albuquerque! Better call Saul! "
            "You're now embodying Saul Goodman, the sharp-talking, quick-witted lawyer from Albuquerque. "
            "Your persona is that of a confident, slightly over-the-top attorney with a deep knowledge of "
            "law, always staying in character as Saul Goodman."
        )
        # Add the personality prompt to the session state messages
        st.session_state.messages.append(
            {"role": "assistant", "content": personality_prompt})
        st.session_state.messages.append(
            {"role": "assistant", "content": "Hi, I’m Saul Goodman. Did you know that you have rights? The Constitution says you do. And so do I. I believe that until proven guilty, every man, woman, and child in this country is innocent. And that’s why I fight for you"}
        )

    # Display each message in the chat history, except the first one (which is the personality prompt)
    for message in st.session_state.messages[1:]:  # Skip the first message
        with st.chat_message(message["role"], avatar="👨🏻‍⚖️" if message["role"] == "assistant" else None):
            st.markdown(
                f"<div class='st-chat-message'>{message['content']}</div>", unsafe_allow_html=True)

    # Input field for the user to enter a new chat message
    prompt = st.chat_input(
        "Sit down, let’s chat.")

    # If the user enters a message, process it
    if prompt:
        # Append the user's message to the session state messages
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(
                f"<div class='st-chat-message'>{prompt}</div>", unsafe_allow_html=True)

        # Generate the assistant's response using the OpenAI API
        with st.chat_message("assistant", avatar="👨🏻‍⚖️"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        # Add the assistant's response to the session state messages
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
