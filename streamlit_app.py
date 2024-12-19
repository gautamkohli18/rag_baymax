import streamlit as st
import google.generativeai as genai
import os

# Set up the Google Generative AI API key
api_key = 'AIzaSyB3n1FTI2oiL_G7M7WqzdroNcQ-dJiFgyA'
os.environ["GOOGLE_API_KEY"] = api_key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

generation_config = { 
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Start the chatbot session
chat_session = model.start_chat(history=[])

# Streamlit app layout
st.title("Baymax")
st.write("Welcome to the chatbot! Type your messages below.")

# Add custom CSS for styling the page, including background image
st.markdown("""
    <style>
        body {
            background-image: url('3334896.jpg');  /* Replace with your image path */
            background-size: cover;
            background-position: center center;
            color: white;
            font-family: 'Helvetica Neue', sans-serif;
            height: 100vh;
            margin: 0;
        }

        .chat-container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.7);  /* Semi-transparent black for readability */
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .message-box {
            display: flex;
            margin: 10px 0;
        }

        .user-message {
            background-color: #ff6b6b;
            color: white;
            padding: 10px 20px;
            border-radius: 15px;
            margin-left: auto;
            max-width: 70%;
            word-wrap: break-word;
        }

        .ai-message {
            background-color: #2e2e2e;
            color: white;
            padding: 10px 20px;
            border-radius: 15px;
            max-width: 70%;
            word-wrap: break-word;
        }

        input[type="text"] {
            background-color: #333;
            color: white;
            border: 1px solid #444;
            padding: 10px 15px;
            border-radius: 5px;
            width: 80%;
            font-size: 16px;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #ff6b6b;
        }

        button {
            background-color: #ff6b6b;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }

        button:hover {
            background-color: #ff4c4c;
        }
    </style>
""", unsafe_allow_html=True)

# Create a container for the chat window
with st.container():
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Display message history
    for message in st.session_state.history:
        if message['role'] == 'user':
            st.markdown(f'<div class="message-box"><div class="user-message">{message["text"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-box"><div class="ai-message">{message["text"]}</div></div>', unsafe_allow_html=True)

    # Input box for user to type their message
    user_input = st.text_input("You: ", "", key="user_input")

    # Send message to the model and display response
    if user_input:
        response = chat_session.send_message(user_input)

        # Append the conversation to the history
        st.session_state.history.append({'role': 'user', 'text': user_input})
        st.session_state.history.append({'role': 'chatbot', 'text': response.text})

        # Display the chatbot's response
        st.markdown(f'<div class="message-box"><div class="ai-message">{response.text}</div></div>', unsafe_allow_html=True)

    # Button to reset the chat
    if st.button('Reset Chat'):
        st.session_state.history = []
        chat_session = model.start_chat(history=[])
        st.write("Chat has been reset.")
