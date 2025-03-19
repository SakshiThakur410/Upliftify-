import streamlit as st
import google.generativeai as genai

# ✅ Fetch API Key Securely from Streamlit Secrets
if "API_KEYS" not in st.secrets or "Gen_API" not in st.secrets["API_KEYS"]:
    st.error("API Key is missing! Please set it in Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["API_KEYS"]["Gen_API"]

# ✅ Configure Gemini API
genai.configure(api_key=API_KEY)

# ✅ Define mood options
MOOD_OPTIONS = [
    "Happy", "Sad", "Anxious", "Stressed", "Excited", "Tired", "Angry", "Bored", "Lonely", "Romantic", "Motivated"
]

DESIRED_FEELINGS = [
    "Relaxed", "Cheerful", "Confident", "Productive", "Loved", "Energetic", "Hopeful", "Inspired", "Excited"
]

# ✅ Function to call Gemini API and get mood suggestions
def get_mood_suggestions(current_feeling, desired_feeling):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Using a fast model
    prompt = f"""
    The user currently feels {current_feeling} and wants to feel {desired_feeling}.
    
    Provide:
    1. A suggestion to transition from {current_feeling} to {desired_feeling}.
    2. A fun activity they can do to improve their mood.
    3. A short motivational message.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text if response else "No suggestion available."
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

# ✅ Streamlit UI
def main():
    st.title("Mood Uplifter App 🎭✨")
    st.write("Select how you're feeling and how you want to feel, and we'll suggest something uplifting!")

    # Dropdown inputs
    current_feeling = st.selectbox("How are you feeling right now?", options=MOOD_OPTIONS)
    desired_feeling = st.selectbox("How would you like to feel?", options=DESIRED_FEELINGS)

    if st.button("Get My Suggestion 🎁"):
        with st.spinner("Thinking of something special for you... 🎭✨"):
            response = get_mood_suggestions(current_feeling, desired_feeling)
            
            if response:
                st.subheader("🌟 Here's what you can do:")
                st.write(response)
            else:
                st.error("Oops! Couldn't fetch a response. Try again!")

if __name__ == "__main__":
    main()
