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

# Initialize OpenAI client with secret
if 'client' not in st.session_state:
    try:
        st.session_state.client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
        )
    except Exception as e:
        st.error("Error initializing OpenAI client. Please check your API key in Streamlit secrets.")
        st.stop()

fine_tuned_model = "ft:gpt-40-2024-08-06:personal:version-1:AXSDq5Hl:ckpt-step-90"

# Page styling
st.set_page_config(
    page_title="Asystent Legitize",
    page_icon="💬",
    layout="wide"
)

# Custom CSS for branding
st.markdown("""
    <style>
        .stApp { background-color: """ + COLORS['light_gray'] + """; }
        header[data-testid="stHeader"] { background-color: """ + COLORS['dark_blue'] + """ !important; }
        .title-text, .subtitle-text { color: """ + COLORS['black'] + """ !important; margin: 0; padding: 0; }
        .stChatMessage { border-radius: 10px; margin-bottom: 1rem; }
        .stChatMessage div, .stChatMessage p, .stChatMessage span { color: """ + COLORS['black'] + """ !important; }
        .stChatMessage[data-testid="user-message"] { background-color: """ + COLORS['dark_blue'] + """ !important; }
        .stChatMessage[data-testid="assistant-message"] { background-color: white !important; border: 2px solid """ + COLORS['yellow'] + """; }
        .stChatInputContainer { position: fixed !important; bottom: 0 !important; left: 0 !important; right: 0 !important; background-color: """ + COLORS['dark_blue'] + """ !important; padding: 20px 60px !important; z-index: 999 !important; }
        textarea { background-color: """ + COLORS['dark_blue'] + """ !important; border: 1px solid """ + COLORS['blue'] + """ !important; color: white !important; }
        textarea::placeholder { color: white !important; opacity: 0.7; }
        .block-container { padding-bottom: 400px !important; }
        .custom-header { background-color: """ + COLORS['dark_blue'] + """ !important; padding: 20px; margin: -100px -100px 20px -100px; }
        .stChatFlow { margin-bottom: 150px !important; }
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
