# At the beginning of your code, after the OpenAI client initialization, add this debug code:

if 'client' not in st.session_state:
    try:
        st.session_state.client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
        )
        print("OpenAI client initialized successfully")
        
        # Enhanced debugging: List available models and check if our model is available
        try:
            models = st.session_state.client.models.list()
            available_models = [model.id for model in models]
            print("Available models:", available_models)
            
            # Your fine-tuned model ID
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

# Then modify the chat completion code section:

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            print(f"Attempting to use fine-tuned model: {fine_tuned_model}")
            print(f"User input: {user_input}")
            
            # Prepare messages
            messages = [
                {
                    "role": "system",
                    "content": "Jesteś asystentem Legitize - firmy oferującej nowoczesne rozwiązania prawne i zarządzanie sprawami prawnymi. Odpowiadaj szczegółowo, profesjonalnie i wyczerpująco na pytania, zawsze odnosząc się do kontekstu prawnego i biznesowego. Na końcu każdej odpowiedzi zachęć do kontaktu z zespołem Legitize w celu uzyskania bardziej szczegółowych informacji lub wsparcia."
                }
            ]
            messages.extend([
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ])
            
            print("Sending request with messages:", messages)
            
            # Make the API call with explicit model parameter
            response = st.session_state.client.chat.completions.create(
                model=fine_tuned_model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                presence_penalty=0.6,
                frequency_penalty=0.4,
            )
            
            # Log the complete response for debugging
            print("Full API Response:", response)
            
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
