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

# ✅ Function to call Gemini API and get suggestions
def get_mood_suggestions(mood, desired_feeling, personality):
    model = genai.GenerativeModel("gemini-2-vision")  # Using latest vision model
    
    prompt = (
        f"You are acting as a {personality}. The user is currently feeling {mood} and wants to feel {desired_feeling}. "
        f"Give personalized advice, comforting words, and fun activity suggestions in an engaging tone."
    )

    try:
        response = model.generate_content(prompt)
        return response.text if response else "I couldn't generate a response. Try again!"
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

# ✅ Function to create a PDF of advice
def generate_pdf(response_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Your Personalized Advice", ln=True, align="C")
    
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, response_text)
    
    pdf_path = "advice.pdf"
    pdf.output(pdf_path)
    return pdf_path

# ✅ Streamlit UI
def main():
    st.set_page_config(page_title="Moody Uplift | Feel Better Now", page_icon="😊", layout="wide")
    
    # 🌟 Beautiful UI
    st.markdown(
        """
        <style>
            body {
                background-color: #f9f9f9;
            }
            .stTitle {
                color: #ff4b4b;
                font-size: 36px;
                text-align: center;
                font-weight: bold;
            }
            .stButton>button {
                background-color: #ff4b4b !important;
                color: white !important;
                font-size: 18px;
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1 class='stTitle'>🎭 Moody Uplift – Get Advice & Fun Activities</h1>", unsafe_allow_html=True)
    st.write("💡 **Choose your mood, get advice, and talk to different personalities!**")

    # 🔥 Mood Selection
    moods = ["Sad", "Happy", "Lonely", "Romantic", "Angry", "Stressed", "Anxious", "Bored", "Excited", "Confused"]
    current_mood = st.selectbox("How are you feeling right now?", moods)

    # 🌈 Desired Emotion Selection
    desired_feelings = ["Loved", "Motivated", "Relaxed", "Confident", "Adventurous", "Playful", "Calm", "Inspired"]
    desired_feeling = st.selectbox("How do you want to feel?", desired_feelings)

    # 🧑‍🤝‍🧑 Personality Selector
    personalities = ["Caring Parent", "Loving Partner", "Best Friend", "Fun Sibling", "Therapist"]
    selected_personality = st.selectbox("Who do you want advice from?", personalities)

    if st.button("Generate Advice & Fun Activities 🎉"):
        st.write("### 📩 Your Input:")
        st.write(f"**Current Mood:** {current_mood}")
        st.write(f"**Desired Feeling:** {desired_feeling}")
        st.write(f"**Selected Personality:** {selected_personality}")

        # ✅ Get Response from Gemini 2.0
        response = get_mood_suggestions(current_mood, desired_feeling, selected_personality)

        if response:
            st.write("### 🌟 Personalized Advice:")
            st.write(response)
            
            # ✅ Generate PDF
            pdf_path = generate_pdf(response)
            with open(pdf_path, "rb") as file:
                st.download_button("📥 Download Advice as PDF", file, file_name="mood_advice.pdf", mime="application/pdf")
        else:
            st.write("⚠️ No advice found. Please try again.")

if __name__ == "__main__":
    main()
