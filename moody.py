import streamlit as st
import requests
import json

# Load Gemini API keys from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_API_URL = st.secrets["GEMINI_API_URL"]

def call_gemini_api(prompt: str, max_tokens: int = 150) -> str:
    """
    Call the Gemini API with the provided prompt and return the response.
    """
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": max_tokens
    }
    response = requests.post(GEMINI_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "")
    else:
        st.error("Error calling Gemini API. Please check your API key and URL.")
        return ""

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
    response_json = call_gemini_api(prompt)
    try:
        response_data = json.loads(response_json)
    except Exception as e:
        st.error("Error parsing Gemini API response. Please try again.")
        response_data = {}
    return response_data

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
