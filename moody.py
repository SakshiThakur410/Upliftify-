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
    You are acting as a {personality}. The user is currently feeling {mood} and wants to feel {desired_feeling}.
    Provide a warm, engaging, and helpful response. Give practical advice and fun activity suggestions.
    Keep the tone natural and conversational.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text if response else "I couldn't generate a response. Try again!"
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

# ✅ Streamlit UI
def main():
    st.set_page_config(page_title="Upliftify – Mood Booster", page_icon="💖", layout="centered")
    
    st.markdown("<h1 style='text-align: center; color: #ff69b4;'>💖 Upliftify – Mood Booster 💖</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #6a5acd;'>Choose your mood and get advice from a special personality!</h3>", unsafe_allow_html=True)
    
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
    
    if st.button("✨ Get Advice"):
        st.markdown("### 💬 Personalized Advice")
        personality_role = personality_options[selected_personality]
        response = get_mood_suggestions(user_mood, target_feeling, personality_role)
        
        if response:
            st.markdown(f"<div style='background-color: #fce4ec; padding: 15px; border-radius: 10px;'><b>{selected_personality}:</b><br>{response}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
