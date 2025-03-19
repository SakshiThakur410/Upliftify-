import streamlit as st
import google.generativeai as genai

# ✅ Fetch API Key Securely from Streamlit Secrets
if "API_KEYS" not in st.secrets or "Gen_API" not in st.secrets["API_KEYS"]:
    st.error("API Key is missing! Please set it in Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["API_KEYS"]["Gen_API"]

# ✅ Configure Gemini API
genai.configure(api_key=API_KEY)

# 🎭 Expanded Mood & Emoji Mapping
MOOD_OPTIONS = {
    "Happy 😊": "😊", "Sad 😢": "😢", "Anxious 😰": "😰", "Stressed 😖": "😖", "Excited 🤩": "🤩",
    "Tired 😴": "😴", "Angry 😠": "😠", "Bored 🥱": "🥱", "Lonely 😞": "😞", "Romantic 💖": "💖",
    "Motivated 🔥": "🔥", "Adventurous 🌍": "🌍", "Sexy 🔥": "🔥", "Confused 🤔": "🤔", "Inspired 🎨": "🎨"
}

DESIRED_FEELINGS = {
    "Relaxed 🌿": "🌿", "Cheerful 😃": "😃", "Confident 💪": "💪", "Productive 📈": "📈", "Loved ❤️": "❤️",
    "Energetic ⚡": "⚡", "Hopeful 🌟": "🌟", "Inspired 🎨": "🎨", "Excited 🎉": "🎉", "Passionate 🔥": "🔥",
    "Playful 😜": "😜", "Romantic 💏": "💏", "Adventurous 🚀": "🚀", "Flirty 😉": "😉"
}

PERSONALITY_OPTIONS = {
    "Caring Friend 👫": "A warm, supportive, and fun friend who understands you.",
    "Loving Partner ❤️": "A romantic, affectionate, and caring partner.",
    "Supportive Parent 👨‍👩‍👧": "A wise, comforting, and protective parent.",
    "Cool Sibling 😎": "A fun, teasing, and chill sibling who lifts your mood.",
    "Motivational Coach 🔥": "A high-energy, no-nonsense coach who fires you up!"
}

# ✅ Function to call Gemini API for mood suggestions
def get_mood_suggestions(current_feeling, desired_feeling, personality):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Using a fast model
    prompt = f"""
    The user currently feels {current_feeling} and wants to feel {desired_feeling}. 
    Respond in the tone of {personality}. 

    Provide:
    1. A thoughtful suggestion in {personality}'s tone to shift from {current_feeling} to {desired_feeling}.
    2. A fun activity they can do.
    3. A short motivational message.
    4. A joke or lighthearted comment in {personality}'s style.
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
            .title {text-align: center; font-size: 2.5em; font-weight: bold; color: #FF69B4;}
            .subtext {text-align: center; font-size: 1.2em; color: #444;}
            .suggestion-box {background-color: #ffffff; padding: 15px; border-radius: 10px; 
                            box-shadow: 0px 0px 15px rgba(0,0,0,0.1);}
            .emoji {font-size: 1.8em; text-align: center;}
            .response-box {background-color: #fdf2e9; padding: 20px; border-radius: 10px; 
                            border-left: 5px solid #FF69B4;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="title">🎭 Mood Uplifter</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtext">Choose your mood and get advice from a special personality! ✨</p>', unsafe_allow_html=True)

    # 🌟 Mood Selection
    col1, col2 = st.columns(2)
    with col1:
        current_feeling = st.selectbox("How are you feeling right now?", options=list(MOOD_OPTIONS.keys()))
    with col2:
        desired_feeling = st.selectbox("How would you like to feel?", options=list(DESIRED_FEELINGS.keys()))

    # 🧑‍🎤 Choose Personality
    personality = st.selectbox("Who do you want advice from?", options=list(PERSONALITY_OPTIONS.keys()))

    # 🌈 Display Mood with Emojis
    st.markdown(f"<p class='emoji'>{MOOD_OPTIONS[current_feeling]} → {DESIRED_FEELINGS[desired_feeling]}</p>", unsafe_allow_html=True)

    # 🎁 Button to Get Suggestion
    if st.button("Get My Personalized Advice 🎁"):
        with st.spinner("Finding the best response... 🎭✨"):
            response = get_mood_suggestions(current_feeling, desired_feeling, personality)
            
            if response:
                st.markdown('<div class="response-box">', unsafe_allow_html=True)
                st.subheader(f"🎭 Response from {personality}:")
                st.write(response)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Oops! Couldn't fetch a response. Try again!")

if __name__ == "__main__":
    main()
