import os
from openai import OpenAI
import streamlit as st

# [Previous code remains the same until the CSS section]

st.markdown("""
    <style>
        /* [Previous CSS rules remain the same until the bottom container section] */

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
            top: 60px !important;  /* Moved higher */
            max-width: 800px !important;
            width: 100% !important;
            margin: 0 auto !important;
            background-color: transparent !important;
            padding: 0 20px !important;
            display: flex !important;
            align-items: center !important;
        }
        
        /* Style the input box and its container */
        .stChatInput {
            display: flex !important;
            align-items: center !important;
            position: relative !important;
            width: 100% !important;
        }
        
        /* Create a wrapper for the input and button */
        .stChatInput > div {
            display: flex !important;
            width: 100% !important;
            border: 1px solid """ + COLORS['blue'] + """ !important;
            border-radius: 4px !important;
            background-color: """ + COLORS['dark_blue'] + """ !important;
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
        }
        
        textarea::placeholder {
            color: white !important;
            opacity: 0.7;
        }
        
        /* Style the send button to be part of the input box */
        button[kind="primary"] {
            height: 45px !important;
            border: none !important;
            border-left: 1px solid """ + COLORS['blue'] + """ !important;
            background-color: """ + COLORS['dark_blue'] + """ !important;
            padding: 0 16px !important;
        }
        
        /* [Rest of the CSS remains the same] */
    </style>
""", unsafe_allow_html=True)

# [Rest of the code remains the same]

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
