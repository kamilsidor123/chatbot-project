import os
from openai import OpenAI
import streamlit as st

# Custom color scheme - using same dark blue for both top and bottom
COLORS = {
    'light_gray': '#F4F4F4',
    'yellow': '#FFD447',
    'black': '#000000',
    'dark_blue': '#003366',  # Using this for both top and bottom
    'blue': '#0055AA',
    'lighter_blue': '#004488'
}

# Initialize OpenAI client with secret
if 'client' not in st.session_state:
    try:
        st.session_state.client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
        )
    except Exception as e:
        st.error("Error initializing OpenAI client. Please check your API key in Streamlit secrets.")
        st.stop()

fine_tuned_model = "ft:gpt-4o-2024-08-06:personal:version-1:AXSDqRcx"

# Page styling
st.set_page_config(
    page_title="Asystent Legitize",
    page_icon="💬",
    layout="wide"
)

# Updated CSS with fixes for bottom bar
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

        /* Create blue background container for input that extends full width */
        div[data-testid="stChatInput"] {
            position: fixed !important;
            bottom: 40px !important;  /* Moved up from bottom */
            left: 0 !important;
            width: 100vw !important;  /* Full viewport width */
            padding: 2rem 0 !important;  /* Removed horizontal padding */
            background-color: """ + COLORS['dark_blue'] + """ !important;
            z-index: 999 !important;
            margin: 0 !important;
            box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* Center the input box */
        div[data-testid="stChatInput"] > div {
            max-width: 800px !important;
            width: 100% !important;
            margin: 0 auto !important;
            background-color: """ + COLORS['dark_blue'] + """ !important;
            padding: 0 20px !important;  /* Add padding to the input container */
        }
        
        /* Style the input box */
        textarea {
            border: 1px solid """ + COLORS['blue'] + """ !important;
            color: white !important;
            background-color: """ + COLORS['dark_blue'] + """ !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
        
        textarea::placeholder {
            color: white !important;
            opacity: 0.7;
        }
        
        /* Content spacing */
        .block-container {
            padding-bottom: 160px !important;  /* Increased to account for raised bottom bar */
        }
        
        /* Header container */
        .custom-header {
            background-color: """ + COLORS['dark_blue'] + """ !important;
            padding: 20px;
            margin: -100px -100px 20px -100px;
        }
        
        /* Chat flow spacing */
        .stChatFlow {
            margin-bottom: 120px !important;  /* Adjusted margin */
            padding-bottom: 50px;
            max-width: 800px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        
        /* Remove white backgrounds from chat input container */
        div[data-testid="stChatInput"] > *, 
        div[data-testid="stChatInput"] div {
            background-color: """ + COLORS['dark_blue'] + """ !important;
        }

        /* Ensure full width coverage */
        .main > div {
            width: 100% !important;
            max-width: 100% !important;
            padding: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Rest of your code remains the same...

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
        full_response = ""

        try:
            # Call OpenAI's chat completion endpoint with new API syntax
            response = st.session_state.client.chat.completions.create(
                model=fine_tuned_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )

            # Extract assistant's reply using new API response structure
            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)

            # Add assistant's response to session state
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"An error occurred: {e}")
