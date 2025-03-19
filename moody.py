import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# ✅ Fetch API Key Securely from Streamlit Secrets
if "API_KEYS" not in st.secrets or "Gen_API" not in st.secrets["API_KEYS"]:
    st.error("API Key is missing! Please set it in Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["API_KEYS"]["Gen_API"]

# ✅ Configure Gemini API
genai.configure(api_key=API_KEY)

def get_mood_response(mood, personality):
    model = genai.GenerativeModel("gemini-2-vision")  # Upgraded to 2.0 Flash Vision
    prompt = (
        f"Act as a {personality} and give comforting advice for someone feeling {mood}. "
        "Also generate a soothing image representing this mood."
    )
    try:
        response = model.generate_content(prompt)
        text_response = response.text if response.text else "No advice available."
        image_response = response.image if hasattr(response, 'image') else None
        return text_response, image_response
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None, None

# ✅ UI Styling
st.markdown(
    """
    <style>
    body {background-color: #f5f7fa;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 10px; font-size: 16px;}
    .stSelectbox, .stTextInput {border-radius: 8px; padding: 5px;}
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Mood and Personality Selection
st.title("🌟 Upliftify – Your Personal Mood Booster")
st.subheader("Choose your mood and get advice from a special personality!")

moods = ["Happy", "Sad", "Romantic", "Anxious", "Excited", "Lonely", "Motivated", "Sexy", "Stressed"]
personalities = {
    "Friend": "Hey! I’m here for you. What’s on your mind?",
    "Parent": "Sweetheart, tell me what’s bothering you.",
    "Partner": "Hey love, let’s make you feel better. 💕",
    "Sibling": "Yo, you seem off. Want to talk?",
    "Therapist": "I’m here to support your mental well-being. What’s on your mind?",
}

selected_mood = st.selectbox("🌈 How are you feeling?", moods)
personality_choice = st.selectbox("👤 Choose a personality:", list(personalities.keys()))
st.write(f"**{personality_choice} says:** {personalities[personality_choice]}")

if st.button("Get Advice & Image"):
    mood_response, mood_image = get_mood_response(selected_mood, personality_choice)
    
    if mood_response:
        st.subheader(f"{personality_choice} says:")
        st.write(mood_response)
    
    if mood_image:
        st.image(mood_image, caption=f"Aesthetic image for '{selected_mood}'", use_column_width=True)

# ✅ Conversational Chat UI
st.subheader("💬 Start a Conversation")
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

user_input = st.text_input("Your Message:")
if user_input:
    st.session_state["conversation"].append(("You", user_input))
    ai_response = get_mood_response(selected_mood, personality_choice)[0]  # Get only text
    st.session_state["conversation"].append((personality_choice, ai_response))

for speaker, message in st.session_state["conversation"]:
    st.chat_message(f"{speaker}: {message}")
