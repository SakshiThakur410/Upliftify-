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

# 🎭 Personality Options
personalities = {
    "Friend": "A cheerful and supportive best friend!",
    "Loving Partner": "A romantic and caring lover!",
    "Sibling": "A fun and teasing sibling!",
    "Parent": "A wise and nurturing parent!",
    "Therapist": "A professional and understanding therapist!"
}

# 🎭 Mood Options
moods = ["Happy", "Sad", "Romantic", "Excited", "Relaxed", "Motivated", "Stressed", "Lonely"]

def get_advice(mood, personality):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = (
        f"You are acting as {personalities[personality]} speaking to someone feeling {mood}. "
        "Provide thoughtful advice with warmth and care."
    )
    try:
        response = model.generate_content(prompt)
        return response.text if response else "No advice available."
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

def generate_image(mood):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Generate an uplifting AI image representing the emotion: {mood}."
    try:
        response = model.generate_content([prompt])
        return response.image if response else None
    except Exception as e:
        st.warning("Couldn't generate an image, but here's some advice instead!")
        return None

# ✅ Streamlit UI
def main():
    st.title("🌟 Upliftify: Personalized Mood Advice")
    st.write("Choose your mood and get advice from a special personality!")

    # 🎭 Mood Selection
    mood = st.selectbox("How are you feeling?", moods)
    personality = st.selectbox("Who would you like advice from?", list(personalities.keys()))

    if st.button("Get Advice!"):
        advice = get_advice(mood, personality)
        ai_image = generate_image(mood)
        
        if ai_image:
            st.image(ai_image, caption=f"A special image to match your mood: {mood}")
        
        if advice:
            st.markdown(f"### 🤗 {personality} says:")
            st.success(advice)
        else:
            st.warning("No advice available. Try again!")

if __name__ == "__main__":
    main()
