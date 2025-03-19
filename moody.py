import streamlit as st
import google.generativeai as genai
import json

# ✅ Fetch API Key Securely from Streamlit Secrets
if "API_KEYS" not in st.secrets or "Gen_API" not in st.secrets["API_KEYS"]:
    st.error("API Key is missing! Please set it in Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["API_KEYS"]["Gen_API"]

# ✅ Configure Gemini API
genai.configure(api_key=API_KEY)

def call_gemini_api(prompt: str) -> dict:
    """
    Call the Gemini API with the provided prompt and return the response as a dictionary.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")  # Using a fast model
    try:
        response = model.generate_content(prompt)
        response_text = response.text if response else "{}"
        return json.loads(response_text)
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return {}

def generate_responses(current_feeling: str, desired_feeling: str, current_mood: str) -> dict:
    """
    Compose a prompt for the Gemini API based on user input and return the parsed JSON response.
    """
    prompt = f"""
    The user provided the following inputs:
    - Current feeling: {current_feeling}
    - Desired feeling: {desired_feeling}
    - Current mood: {current_mood}
    
    Based on these inputs, please provide:
    1. A tailored suggestion on what the user can do to improve their mood.
    2. A personalized motivational message.
    3. A joke if the user is feeling down (if not, leave it empty).
    
    Format your response as a JSON object with keys: "suggestion", "motivational_message", and "joke".
    """
    return call_gemini_api(prompt)

def main():
    st.title("Mood Uplifter App with Gemini API")
    st.write("Enter your current state below and let our app generate a suggestion, motivational message, and even a joke to brighten your day!")

    # Collect user input
    current_feeling = st.text_input("How are you feeling right now?")
    desired_feeling = st.text_input("How would you like to feel?")
    current_mood = st.text_input("What is your current mood?")

    if st.button("Get My Suggestion"):
        if not current_feeling or not desired_feeling or not current_mood:
            st.error("Please fill in all fields to get a complete response.")
        else:
            with st.spinner("Generating your personalized response..."):
                response_data = generate_responses(current_feeling, desired_feeling, current_mood)
                suggestion = response_data.get("suggestion", "No suggestion provided.")
                motivational_message = response_data.get("motivational_message", "No motivational message provided.")
                joke = response_data.get("joke", "")
                
                st.subheader("Your Suggestion:")
                st.write(suggestion)
                
                st.subheader("Motivational Message:")
                st.write(motivational_message)
                
                if joke:
                    st.subheader("A Little Joke:")
                    st.write(joke)

if __name__ == "__main__":
    main()
