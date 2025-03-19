import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# ✅ Fetch API Key Securely from Streamlit Secrets
if "API_KEYS" not in st.secrets or "Gen_API" not in st.secrets["API_KEYS"]:
    st.error("API Key is missing! Please set it in Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["API_KEYS"]["Gen_API"]

# ✅ Configure Gemini API
genai.configure(api_key=API_KEY)

def get_advice(mood, desired_feeling, personality, user_message):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"You are acting as {personality}. Your user is feeling {mood} and wants to feel {desired_feeling}.\n\n"
        f"They said: '{user_message}'.\n\n"
        "Give a thoughtful, engaging, and warm response to uplift their mood."
    )
    
    try:
        response = model.generate_content(prompt)
        return response.text if response else "I don't have advice right now. Try again!"
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

# ✅ Streamlit UI
def main():
    st.set_page_config(page_title="Mood Uplifter", page_icon="😊", layout="centered")
    
    st.title("🌟 Mood Uplifter – Feel Better Instantly!")
    st.write("Choose your mood, select a personality, and get heartfelt advice! 💖")
    
    # 🎭 Mood Selection
    moods = ["Happy", "Sad", "Romantic", "Angry", "Sexy", "Anxious", "Lonely", "Frustrated", "Excited"]
    mood = st.selectbox("How are you feeling right now?", options=moods)
    
    desired_feelings = ["Relaxed", "Loved", "Motivated", "Confident", "Joyful", "Peaceful", "Romantic", "Cheerful"]
    desired_feeling = st.selectbox("How would you like to feel?", options=desired_feelings)
    
    # 👥 Personality Selector
    personalities = {
        "Friend": "A supportive, fun-loving best friend",
        "Parent": "A wise, caring parent",
        "Partner": "A loving, romantic partner",
        "Sibling": "A playful and understanding sibling",
        "Therapist": "A professional therapist providing mental support"
    }
    personality = st.selectbox("Who do you want advice from?", options=list(personalities.keys()))
    
    # 🗨️ Chat UI
    st.write("## 💬 Talk to Your Chosen Personality")
    user_message = st.text_area("Type your message or concern:", placeholder="Tell me what's on your mind...")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if st.button("Send"):
        if user_message:
            with st.spinner("Thinking... 🎭✨"):
                response = get_advice(mood, desired_feeling, personality, user_message)
                if response:
                    st.session_state.chat_history.append({"role": "You", "text": user_message})
                    st.session_state.chat_history.append({"role": personality, "text": response})
                    st.rerun()  # ✅ Updated from st.experimental_rerun()
    
    # Display chat history beautifully
    st.write("## 📝 Conversation")
    for chat in st.session_state.chat_history:
        role, text = chat["role"], chat["text"]
        if role == "You":
            st.markdown(f"**🧑‍💻 You:** {text}")
        else:
            st.markdown(f"**🎭 {role}:** {text}")
    
if __name__ == "__main__":
    main()
