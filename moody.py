import streamlit as st
import google.generativeai as genai

# ✅ Fetch API Key Securely from Streamlit Secrets
if "API_KEYS" not in st.secrets or "Gen_API" not in st.secrets["API_KEYS"]:
    st.error("API Key is missing! Please set it in Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["API_KEYS"]["Gen_API"]

# ✅ Configure Gemini API
genai.configure(api_key=API_KEY)

# 🎭 Mood & Emoji Mapping
MOOD_OPTIONS = {
    "Happy": "😊", "Sad": "😢", "Anxious": "😰", "Stressed": "😖", "Excited": "🤩",
    "Tired": "😴", "Angry": "😠", "Bored": "🥱", "Lonely": "😞", "Romantic": "💖", "Motivated": "🔥"
}

DESIRED_FEELINGS = {
    "Relaxed": "🌿", "Cheerful": "😃", "Confident": "💪", "Productive": "📈", "Loved": "❤️",
    "Energetic": "⚡", "Hopeful": "🌟", "Inspired": "🎨", "Excited": "🎉"
}

# ✅ Function to call Gemini API for mood suggestions
def get_mood_suggestions(current_feeling, desired_feeling):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Using a fast model
    prompt = f"""
    The user currently feels {current_feeling} and wants to feel {desired_feeling}.
    
    Provide:
    1. A thoughtful suggestion to transition from {current_feeling} to {desired_feeling}.
    2. A fun activity they can do to improve their mood.
    3. A short, motivational message in an inspiring tone.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text if response else "No suggestion available."
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

# ✅ Streamlit UI - Enhanced
def main():
    st.set_page_config(page_title="Mood Uplifter", page_icon="🎭", layout="centered")
    
    # 🌟 Custom Styles
    st.markdown("""
        <style>
            .main {background-color: #f8f9fa;}
            .title {text-align: center; font-size: 2.2em; font-weight: bold; color: #4CAF50;}
            .subtext {text-align: center; font-size: 1.2em; color: #555;}
            .suggestion-box {background-color: #ffffff; padding: 15px; border-radius: 10px; 
                            box-shadow: 0px 0px 15px rgba(0,0,0,0.1);}
            .emoji {font-size: 1.8em;}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="title">🎭 Mood Uplifter App</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtext">Select how you feel and let us uplift your mood! 🌟</p>', unsafe_allow_html=True)
    
    # 🌟 Mood Selection
    col1, col2 = st.columns(2)
    with col1:
        current_feeling = st.selectbox("How are you feeling right now?", options=MOOD_OPTIONS.keys())
    with col2:
        desired_feeling = st.selectbox("How would you like to feel?", options=DESIRED_FEELINGS.keys())
    
    # 🌈 Display Mood with Emojis
    st.markdown(f"<p class='emoji'>{MOOD_OPTIONS[current_feeling]} → {DESIRED_FEELINGS[desired_feeling]}</p>", unsafe_allow_html=True)

    # 🎁 Button to Get Suggestion
    if st.button("Get My Suggestion 🎁"):
        with st.spinner("Finding something special for you... 🎭✨"):
            response = get_mood_suggestions(current_feeling, desired_feeling)
            
            if response:
                st.markdown('<div class="suggestion-box">', unsafe_allow_html=True)
                st.subheader(f"🌟 Your Personalized Suggestion:")
                st.write(response)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Oops! Couldn't fetch a response. Try again!")

if __name__ == "__main__":
    main()
