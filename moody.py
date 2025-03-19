import streamlit as st
import google.generativeai as genai

# ✅ Secure API Key Configuration
if "API_KEYS" not in st.secrets or "Gen_API" not in st.secrets["API_KEYS"]:
    st.error("API Key is missing! Please set it in Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["API_KEYS"]["Gen_API"]

# ✅ Configure Gemini API
genai.configure(api_key=API_KEY)

# 🎭 Expanded Personality and Mood Options
PERSONALITY_OPTIONS = {
    "Caring Friend 👫": "A warm, supportive, and fun friend who understands you.",
    "Loving Partner ❤️": "A romantic, affectionate, and caring partner.",
    "Supportive Parent 👨‍👩‍👧": "A wise, comforting, and protective parent.",
    "Cool Sibling 😎": "A fun, teasing, and chill sibling who lifts your mood.",
    "Motivational Coach 🔥": "A high-energy, no-nonsense coach who fires you up!",
    "Therapist 🧠": "A professional and empathetic therapist who provides emotional support."
}

MOODS = ["Happy 😊", "Sad 😢", "Anxious 😰", "Stressed 😖", "Excited 🤩", "Tired 😴", 
         "Angry 😠", "Bored 🥱", "Lonely 😞", "Romantic 💖", "Motivated 🔥", 
         "Adventurous 🌍", "Sexy 🔥", "Confused 🤔", "Inspired 🎨"]

DESIRED_FEELINGS = ["Relaxed 🌿", "Cheerful 😃", "Confident 💪", "Productive 📈", "Loved ❤️",
                    "Energetic ⚡", "Hopeful 🌟", "Inspired 🎨", "Excited 🎉", "Passionate 🔥",
                    "Playful 😜", "Romantic 💏", "Adventurous 🚀", "Flirty 😉"]

# ✅ Function to Call Gemini API for Mood-Based Advice
def get_mood_suggestions(current_feeling, desired_feeling, personality):
    model = genai.GenerativeModel("gemini-1.5-flash")  
    prompt = f"""
    You are {personality}. The user currently feels {current_feeling} and wants to feel {desired_feeling}. 

    Provide:
    1. Thoughtful advice in {personality}'s unique tone.
    2. A fun activity suggestion.
    3. A motivational message.
    4. A joke or lighthearted comment in {personality}'s style.
    """

    try:
        response = model.generate_content(prompt)
        return response.text if response else "No suggestion available."
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

# ✅ Function to Handle Conversational AI
def chat_with_personality(personality, user_message):
    model = genai.GenerativeModel("gemini-1.5-flash")  
    prompt = f"""
    You are {personality}. You are chatting with a user. 
    Respond naturally and in {personality}'s style. 
    Make the conversation engaging and supportive.
    
    User: {user_message}
    """

    try:
        response = model.generate_content(prompt)
        return response.text if response else "Hmm... I don't know what to say!"
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

# ✅ Streamlit UI - Enhanced Conversational Mode
def main():
    st.set_page_config(page_title="Mood Uplifter & Chat AI", page_icon="🎭", layout="wide")

    # 🌟 Custom Styles
    st.markdown("""
        <style>
            .main {background-color: #f8f9fa;}
            .title {text-align: center; font-size: 2.5em; font-weight: bold; color: #FF69B4;}
            .subtext {text-align: center; font-size: 1.2em; color: #444;}
            .chat-container {max-height: 400px; overflow-y: auto; padding: 10px; background-color: #fdf2e9; border-radius: 10px; margin-top: 10px;}
            .chat-message {padding: 10px; border-radius: 5px; margin: 5px 0; background-color: #ffffff;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="title">🎭 Mood Uplifter & AI Chat</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtext">Choose advice or have a real conversation with a personality of your choice! ✨</p>', unsafe_allow_html=True)

    # 🌟 Mode Selection
    mode = st.radio("How would you like to interact?", ["Advice Based on Mood 🧘", "Chat with AI 💬"])

    if mode == "Advice Based on Mood 🧘":
        col1, col2 = st.columns(2)
        with col1:
            current_feeling = st.selectbox("How are you feeling?", options=MOODS)
        with col2:
            desired_feeling = st.selectbox("How would you like to feel?", options=DESIRED_FEELINGS)

        personality = st.selectbox("Choose a personality for your advice:", options=list(PERSONALITY_OPTIONS.keys()))

        if st.button("Get Advice 🎁"):
            with st.spinner("Thinking... 🎭✨"):
                response = get_mood_suggestions(current_feeling, desired_feeling, personality)
                
                if response:
                    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                    st.subheader(f"🎭 {personality} says:")
                    st.write(response)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("Oops! Couldn't fetch a response. Try again!")

    elif mode == "Chat with AI 💬":
        personality = st.selectbox("Choose a personality for chat:", options=list(PERSONALITY_OPTIONS.keys()))

        # Chat History
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            st.markdown(f'<div class="chat-message"><b>{msg["role"]}:</b> {msg["text"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # User Input
        user_message = st.text_input("Type your message...", placeholder="Start chatting with your chosen personality!")

        if st.button("Send"):
            if user_message:
                with st.spinner("Thinking... 🎭✨"):
                    response = chat_with_personality(personality, user_message)
                    if response:
                        st.session_state.chat_history.append({"role": "You", "text": user_message})
                        st.session_state.chat_history.append({"role": personality, "text": response})
                        st.experimental_rerun()
            else:
                st.warning("Please type a message to start the chat!")

if __name__ == "__main__":
    main()
