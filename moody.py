import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# ✅ Secure API Key Fetching
if "API_KEYS" not in st.secrets or "Gen_API" not in st.secrets["API_KEYS"]:
    st.error("API Key is missing! Please set it in Streamlit secrets.")
    st.stop()
API_KEY = st.secrets["API_KEYS"]["Gen_API"]

# ✅ Configure Gemini API
genai.configure(api_key=API_KEY)

def get_mood_response(mood, desired_feeling, personality):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"You are acting as a {personality}. Give an engaging and comforting response for someone who is feeling {mood} 
        and wants to feel {desired_feeling}. Make the response interactive and supportive."
    )
    
    try:
        response = model.generate_content(prompt)
        return response.text if response else "I don't have an answer right now. Try again!"
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

def generate_pdf(response_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Your Personalized Advice", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, response_text)
    pdf_path = "mood_advice.pdf"
    pdf.output(pdf_path)
    return pdf_path

def main():
    st.set_page_config(page_title="Moody - Uplift Your Mood", page_icon="😊", layout="centered")
    
    # 🎨 Custom Styling
    st.markdown("""
        <style>
            body { background-color: #f8f9fa; }
            .big-font { font-size:20px !important; }
            .stButton>button { border-radius: 25px; padding: 10px 20px; background: linear-gradient(135deg, #ff9a9e, #fad0c4); color: white; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
    
    # 🎭 **Header with Emojis**
    st.title("🌈 Moody - Lift Your Mood Instantly!")
    st.write("Choose your mood and get advice from a special personality! 💬")
    
    # 🎭 **Mood & Personality Selectors**
    mood = st.selectbox("How are you feeling right now?", ["Happy", "Sad", "Motivated", "Romantic", "Sexy", "Stressed", "Bored", "Anxious"])
    desired_feeling = st.selectbox("How would you like to feel?", ["Happy", "Relaxed", "Inspired", "Confident", "Loved", "Excited", "Peaceful", "Focused"])
    personality = st.radio("Who do you want advice from?", ["A supportive Friend", "A loving Partner", "A caring Parent", "A fun Sibling", "A professional Therapist"])
    
    # 🎯 **Generate Response**
    if st.button("Get Advice ✨"):
        with st.spinner("Fetching your personalized advice..."):
            response = get_mood_response(mood, desired_feeling, personality)
        
        if response:
            st.success("Here's your uplifting advice:")
            st.markdown(f"<p class='big-font'>{response}</p>", unsafe_allow_html=True)
            
            # 📥 **Download PDF Option**
            pdf_path = generate_pdf(response)
            with open(pdf_path, "rb") as file:
                st.download_button("📄 Download Advice as PDF", file, file_name="mood_advice.pdf", mime="application/pdf")
        else:
            st.error("No response generated. Please try again.")

if __name__ == "__main__":
    main()
