import streamlit as st
import google.generativeai as genai

# ✅ Securely fetch API key from Streamlit Secrets
if "API_KEYS" not in st.secrets or "Gen_API" not in st.secrets["API_KEYS"]:
    st.error("API Key is missing! Please set it in Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["API_KEYS"]["Gen_API"]

# ✅ Configure Gemini API
genai.configure(api_key=API_KEY)

# ✅ Function for realistic, context-aware chat
def get_chat_response(personality, user_input, chat_history):
    model = genai.GenerativeModel("gemini-1.5-flash")

    # If the input is simple (like "hi"), return a short response
    casual_responses = {
        "hi": "Hey! 😊 How's your day going?",
        "hello": "Hello! 👋 What's up?",
        "hey": "Hey there! How can I help?",
        "how are you": "I'm doing great! Thanks for asking. How about you?",
        "what's up": "Not much, just here to chat with you! What’s on your mind?",
    }

    lower_input = user_input.strip().lower()

    if lower_input in casual_responses:
        return casual_responses[lower_input]  # Return short, casual response

    # If the message needs a deeper response
    conversation_history = "\n".join(f"{role}: {text}" for role, text in chat_history)

    prompt = f"""
    You are acting as {personality}. Have a **natural, engaging, and human-like** conversation.
    - **Short, casual replies** for greetings like "hi", "hello".
    - **Deeper responses** when user asks about emotional topics.
    - **Do NOT be overly formal or robotic**. Keep it **friendly and real**.

    Previous messages:
    {conversation_history}

    User: {user_input}
    AI:
    """

    try:
        response = model.generate_content(prompt)
        return response.text if response else "I couldn't generate a response. Try again!"
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

# ✅ Streamlit UI
def main():
    st.set_page_config(page_title="Upliftify – Real Human-Like AI Chat", page_icon="💖", layout="centered")

    # 🎭 Personality Selection
    personality_options = {
        "Friendly Buddy": "a warm, caring, and uplifting friend",
        "Loving Partner": "a deeply affectionate and understanding partner",
        "Wise Parent": "a comforting, wise, and patient parent",
        "Fun Sibling": "a playful yet caring and supportive sibling",
        "Therapist": "a professional therapist offering deep emotional guidance"
    }
    
    selected_personality = st.selectbox("💬 Choose a Personality", list(personality_options.keys()))

    # ✅ Chat Feature
    st.markdown("## 🗨️ Chat with Your Chosen Personality")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display previous messages
    for msg in st.session_state.chat_history:
        role, text = msg
        color = "#ff4081" if role == "You" else "#B39DDB"
        st.markdown(f"<div class='chat-box' style='color: {color};'><b>{role}:</b> {text}</div>", unsafe_allow_html=True)

    # Input for new message
    user_input = st.text_input("Type your message...")
    
    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append(("You", user_input))
            ai_response = get_chat_response(personality_options[selected_personality], user_input, st.session_state.chat_history)
            
            if ai_response:
                st.session_state.chat_history.append((selected_personality, ai_response))
                st.rerun()  # ✅ FIXED: Using st.rerun() instead of experimental_rerun()

if __name__ == "__main__":
    main()
