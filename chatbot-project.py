import os
from openai import OpenAI
import streamlit as st

# Custom color scheme
COLORS = {
    'light_gray': '#F4F4F4',
    'yellow': '#FFD447',
    'black': '#000000',
    'dark_blue': '#003366',
    'blue': '#0055AA',
    'lighter_blue': '#004488'
}

# Initialize OpenAI client with secret and debug model list
if 'client' not in st.session_state:
    try:
        st.session_state.client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
        )
        print("OpenAI client initialized successfully")
        
        # Debug: List available models and check if our model is available
        try:
            models = st.session_state.client.models.list()
            available_models = [model.id for model in models]
            print("Available models:", available_models)
            
            # Updated fine-tuned model ID
            fine_tuned_model = "ft:gpt-4o-2024-08-06:personal:final-version-1:AXr7ilG1"
            
            if fine_tuned_model in available_models:
                print(f"✓ Fine-tuned model {fine_tuned_model} is available")
            else:
                print(f"✗ Fine-tuned model {fine_tuned_model} not found in available models")
                print("Please check if the model ID is correct")
                
        except Exception as e:
            print(f"Error listing models: {e}")
            
    except Exception as e:
        error_message = f"Error initializing OpenAI client: {str(e)}"
        print(error_message)
        st.error("Error initializing OpenAI client. Please check your API key in Streamlit secrets.")
        st.stop()

# Use the updated fine-tuned model ID
fine_tuned_model = "ft:gpt-4o-2024-08-06:personal:final-version-1:AXr7ilG1"

# Page styling
st.set_page_config(
    page_title="Asystent Legitize",
    page_icon="💬",
    layout="wide"
)

# Updated CSS with enhanced styling
st.markdown("""
    <style>
        /* Main app background */
        .stApp {
            background-color: """ + COLORS['light_gray'] + """;
        }
        
        /* Header styling */
        header[data-testid="stHeader"] {
            background-color: """ + COLORS['dark_blue'] + """ !important;
        }
        
        /* Text styling */
        .title-text, .subtitle-text {
            color: """ + COLORS['black'] + """ !important;
            margin: 0;
            padding: 0;
        }
        
        /* Chat messages */
        .stChatMessage {
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .stChatMessage div, .stChatMessage p, .stChatMessage span {
            color: """ + COLORS['black'] + """ !important;
        }
        
        .stChatMessage[data-testid="user-message"] {
            background-color: """ + COLORS['dark_blue'] + """ !important;
        }
        
        .stChatMessage[data-testid="assistant-message"] {
            background-color: white !important;
            border: 2px solid """ + COLORS['yellow'] + """;
        }

        /* Bottom container with full coverage */
        .stChatInputContainer, div[data-testid="stChatInput"] {
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            background-color: """ + COLORS['dark_blue'] + """ !important;
            z-index: 999 !important;
            margin: 0 !important;
            padding: 0 !important;
            border-radius: 0 !important;
            height: 180px !important;
        }

        /* Input container positioning */
        div[data-testid="stChatInput"] > div {
            position: relative !important;
            top: 10px !important;
            max-width: 700px !important;
            width: 100% !important;
            margin: 0 auto !important;
            background-color: transparent !important;
            padding: 0 20px !important;
            display: flex !important;
            align-items: center !important;
        }
        
        /* Style the input box with complete right border */
        .stChatInput {
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 4px !important;
            overflow: hidden !important;
            position: relative !important;
            padding: 0 !important;
            margin: 0 !important;
            background-color: """ + COLORS['dark_blue'] + """ !important;
        }
        
        .stChatInput > div {
            display: flex !important;
            width: 100% !important;
            border: none !important;
            background: none !important;
            box-shadow: none !important;
        }
        
        textarea {
            border: none !important;
            color: white !important;
            background-color: """ + COLORS['dark_blue'] + """ !important;
            padding: 12px 16px !important;
            margin: 0 !important;
            height: 45px !important;
            min-height: 45px !important;
            max-height: 45px !important;
            resize: none !important;
            flex-grow: 1 !important;
            font-size: 14px !important;
            box-shadow: none !important;
        }
        
        textarea::placeholder {
            color: white !important;
            opacity: 0.7;
        }
        
        /* Style the send button with complete borders */
        button[kind="primary"] {
            height: 45px !important;
            background-color: """ + COLORS['dark_blue'] + """ !important;
            padding: 0 16px !important;
            margin: 0 !important;
            box-shadow: none !important;
            border: none !important;
            border-left: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
            position: relative !important;
            border-radius: 0 3px 3px 0 !important;
        }

        /* Remove default button hover effects */
        button[kind="primary"]:hover {
            border-left: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
            background-color: """ + COLORS['dark_blue'] + """ !important;
        }
        
        /* Content spacing */
        .block-container {
            padding-bottom: 200px !important;
        }
        
        /* Header container */
        .custom-header {
            background-color: """ + COLORS['dark_blue'] + """ !important;
            padding: 20px;
            margin: -100px -100px 20px -100px;
            max-width: 100vw !important;
        }

        .custom-header > div {
            max-width: 700px !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding: 0 20px !important;
        }
        
        /* Chat flow spacing */
        .stChatFlow {
            margin-bottom: 200px !important;
            padding-bottom: 50px;
            max-width: 700px !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-left: 20px !important;
            padding-right: 20px !important;
        }
        
        /* Remove any rounded corners and ensure dark blue background */
        div[data-testid="stChatInput"] > *, 
        div[data-testid="stChatInput"] div,
        .stChatInputContainer > *,
        .stChatInputContainer div {
            background-color: """ + COLORS['dark_blue'] + """ !important;
        }

        /* Ensure full width coverage */
        .main > div {
            width: 100% !important;
            max-width: 100% !important;
            padding: 0 !important;
        }

        /* Remove any default border radius */
        .stChatFloatingInputContainer {
            border-radius: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create header container
st.markdown('<div class="custom-header">', unsafe_allow_html=True)

# Create two columns for logo and title
col1, col2 = st.columns([1, 4])

# Add logo in the first column
with col1:
    st.image("Legitize logo new (1).png", width=150)

# Add title and subtitle in the second column
with col2:
    st.markdown('<h1 class="title-text">Asystent Legitize</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">W czym mogę Ci dzisiaj pomóc?</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("Wpisz swoje pytanie tutaj..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            print(f"Attempting to use fine-tuned model: {fine_tuned_model}")
            print(f"User input: {user_input}")
            
            # Prepare messages with system prompt matching the fine-tuned format
            messages = [
                {
                    "role": "system",
                    "content": [{
                        "type": "text",
                        "text": "Jesteś specjalistą w Legitize – firmie zajmującej się doradzaniem szefom działów prawnych w jaki sposób mogą ułożyć i zoptymalizować pracę swojego zespołu. Usługa polega na mapowaniu procesów, lokalizowania blokerów i wąskich gardeł, rekomendacjach w zakresie wyboru narzędzi wspierających zarządzanie pracą zespołów i projektów prawnych, a także automatyzacji manualnych i czasochłonnych zadań. Naszym głównym celem jest poszukiwanie rozwiązań dopasowanych do klienta pod kątem jego potrzeb, umiejętności technologicznych oraz możliwości budżetowych.\nKażda odpowiedź na pytanie powinna być w profesjonalnym tonie na poziomie executive. Unikaj sformułowań związanych typowo z żargonem IT i zarządzaniem projektami. Wypowiedź powinna być konkretna na maks. 1500 znaków. \n"
                    }]
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            
            print("Sending request with model:", fine_tuned_model)
            
            # Make the API call with matching parameters from the example
            response = st.session_state.client.chat.completions.create(
                model=fine_tuned_model,
                messages=messages,
                response_format={"type": "text"},
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            print("Response model:", response.model)  # Log which model actually responded
            
            full_response = response.choices[0].message.content
            print(f"Response received: {full_response[:100]}...")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(error_message)
            print("Full error details:", str(e))
            st.error(error_message)
            print("Current session state messages:", st.session_state.messages)
