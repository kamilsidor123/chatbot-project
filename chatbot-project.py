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
        
        # Debug: List available models
        try:
            models = st.session_state.client.models.list()
            print("Available models:", [model.id for model in models])
        except Exception as e:
            print(f"Error listing models: {e}")
            
    except Exception as e:
        error_message = f"Error initializing OpenAI client: {str(e)}"
        print(error_message)
        st.error("Error initializing OpenAI client. Please check your API key in Streamlit secrets.")
        st.stop()

# Use exact fine-tuned model ID
fine_tuned_model = "ft:gpt-4o-2024-08-06:personal:version-1:AXSDqRcx"

# Page styling
st.set_page_config(
    page_title="Asystent Legitize",
    page_icon="💬",
    layout="wide"
)

# Updated CSS with fixed circuit border
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
            max-width: 800px !important;
            width: 100% !important;
            margin: 0 auto !important;
            background-color: transparent !important;
            padding: 0 20px !important;
            display: flex !important;
            align-items: center !important;
        }
        
        /* Style the input box and its container with complete circuit */
        .stChatInput {
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 4px !important;
            overflow: visible !important;
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
        
        /* Style the send button as part of the circuit */
        button[kind="primary"] {
            height: 45px !important;
            background-color: """ + COLORS['dark_blue'] + """ !important;
            padding: 0 16px !important;
            margin: 0 !important;
            box-shadow: none !important;
            border: none !important;
            border-left: 1px solid rgba(255, 255, 255, 0.2) !important;
            position: relative !important;
            border-radius: 0 3px 3px 0 !important;
        }

        /* Remove default button hover effects */
        button[kind="primary"]:hover {
            border-left: 1px solid rgba(255, 255, 255, 0.2) !important;
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
        }
        
        /* Chat flow spacing */
        .stChatFlow {
            margin-bottom: 200px !important;
            padding-bottom: 50px;
            max-width: 800px !important;
            margin-left: auto !important;
            margin-right: auto !important;
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
            
            # Enhanced API call with more specific parameters
            response = st.session_state.client.chat.completions.create(
                model=fine_tuned_model,
                messages=[
                    # Add a system message to set the context and expected behavior
                    {
                        "role": "system",
                        "content": "Jesteś asystentem Legitize - firmy oferującej nowoczesne rozwiązania prawne i zarządzanie sprawami prawnymi. Odpowiadaj szczegółowo, profesjonalnie i wyczerpująco na pytania, zawsze odnosząc się do kontekstu prawnego i biznesowego. Na końcu każdej odpowiedzi zachęć do kontaktu z zespołem Legitize w celu uzyskania bardziej szczegółowych informacji lub wsparcia."
                    }
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.7,
                max_tokens=2000,  # Increase max tokens for longer responses
                presence_penalty=0.6,  # Encourage more diverse responses
                frequency_penalty=0.4,  # Reduce repetition
            )
            
            full_response = response.choices[0].message.content
            print(f"Response received: {full_response[:100]}...")  # Log first 100 chars
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(error_message)  # Log the error
            st.error(error_message)
            # Optionally, log additional debugging information
            print("Current session state messages:", st.session_state.messages)
