import streamlit as st
import google.generativeai as genai

# ✅ Securely fetch API key from Streamlit Secrets
if "API_KEYS" not in st.secrets or "Gen_API" not in st.secrets["API_KEYS"]:
    st.error("API Key is missing! Please set it in Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["API_KEYS"]["Gen_API"]

# ✅ Configure Gemini API
genai.configure(api_key=API_KEY)

# ✅ Function to get mood-based suggestions from Gemini
def get_mood_suggestions(mood, desired_feeling, personality):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Fast text-based model
    
    prompt = f"""
    You are acting as {personality}. The user is currently feeling {mood} and wants to feel {desired_feeling}.
    Provide a warm, engaging, and helpful response. Keep the tone natural and conversational.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text if response else "I couldn't generate a response. Try again!"
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

# ✅ Function to handle live chat
def get_chat_response(personality, user_input, chat_history):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    conversation_history = "\n".join(f"{role}: {text}" for role, text in chat_history)
    prompt = f"""
    You are acting as {personality}. Have a supportive and engaging conversation with the user.
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
    st.set_page_config(page_title="Upliftify – Mood Booster & Chat", page_icon="💖", layout="centered")

    # 🎨 Dark Mode Styling
    dark_theme_style = """
        <style>
            body { background-color: #121212; color: #E0E0E0; }
            .stTextInput, .stSelectbox, .stButton { color: #E0E0E0; background-color: #1E1E1E; }
            .stMarkdown { color: #E0E0E0; }
            .response-box { background-color: #222; padding: 15px; border-radius: 10px; border: 1px solid #444; }
            .chat-box { background-color: #333; padding: 10px; border-radius: 10px; border: 1px solid #555; margin-bottom: 10px; }
        </style>
    """
    st.markdown(dark_theme_style, unsafe_allow_html=True)
    
    # 🏠 App Title
    st.markdown("<h1 style='text-align: center; color: #ff4081;'>💖 Upliftify – Mood Booster & Chat 💖</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #B39DDB;'>Choose your mood, get advice, or have a conversation with a special personality!</h3>", unsafe_allow_html=True)
    
    # 🎭 Personality Selection
    personality_options = {
        "Friendly Buddy": "a caring and cheerful friend",
        "Loving Partner": "a romantic and affectionate partner",
        "Wise Parent": "a thoughtful and understanding parent",
        "Fun Sibling": "a playful and supportive sibling",
        "Therapist": "a professional therapist offering mindful guidance"
    }
    
    selected_personality = st.selectbox("💬 Choose a Personality", list(personality_options.keys()))

    # 🎭 Mood Selection
    mood_options = ["Sad", "Stressed", "Lonely", "Angry", "Anxious", "Lost", "Unmotivated", "Romantic", "Sexy", "Excited"]
    user_mood = st.selectbox("😔 How are you feeling right now?", mood_options)
    
    # 🎯 Desired Feeling
    desired_feelings = ["Happy", "Relaxed", "Loved", "Motivated", "Confident", "Adventurous", "Romantic", "Energetic"]
    target_feeling = st.selectbox("🌟 How do you want to feel?", desired_feelings)
    
    # ✅ Advice Section
    if st.button("✨ Get Personalized Advice"):
        st.markdown("### 💬 Personalized Advice")
        personality_role = personality_options[selected_personality]
        response = get_mood_suggestions(user_mood, target_feeling, personality_role)
        
        if response:
            st.markdown(f"<div class='response-box'><b>{selected_personality}:</b><br>{response}</div>", unsafe_allow_html=True)

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
                st.experimental_rerun()

if __name__ == "__main__":
    main()
