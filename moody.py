import streamlit as st

# Define a function to generate suggestions based on input mood
def get_suggestion(current_mood, desired_mood):
    # Convert mood to lowercase for consistency
    mood = current_mood.lower().strip()
    
    # Basic logic for different moods; feel free to expand or use more sophisticated logic.
    if mood in ["sad", "down", "depressed"]:
        suggestion = "Maybe try watching a comedy show or go for a quick walk to clear your mind."
        joke = "Here's a joke: Why don't scientists trust atoms? Because they make up everything!"
    elif mood in ["happy", "excited", "joyful"]:
        suggestion = "Keep shining! How about sharing your positivity with a friend or trying something creative?"
        joke = None  # No joke if you're already happy
    else:
        suggestion = "Consider some mindfulness exercises or meditation to enhance your well-being."
        joke = "Here's a light-hearted joke: Why did the tomato blush? Because it saw the salad dressing!"
    
    # Return both suggestion and joke
    return suggestion, joke

# Define a function to generate a motivational message
def get_motivational_message():
    return "Believe in yourself and all that you are. Remember, there's something inside you that's greater than any obstacle!"

# App Title and Introduction
st.title("Mood Uplifter App")
st.write("Welcome! This app asks about your feelings and mood, then provides tailored suggestions, motivational messages, and even a joke to brighten your day.")

# Input fields for user responses
current_feeling = st.text_input("How are you feeling right now?")
desired_feeling = st.text_input("How would you like to feel?")
current_mood = st.text_input("What is your current mood?")

# Button to trigger suggestion generation
if st.button("Get My Suggestion"):
    if not current_mood:
        st.error("Please tell us your current mood to get a suggestion.")
    else:
        suggestion, joke = get_suggestion(current_mood, desired_feeling)
        motivational_message = get_motivational_message()
        
        # Display the outputs
        st.subheader("Your Suggestion:")
        st.write(suggestion)
        
        st.subheader("Motivational Message:")
        st.write(motivational_message)
        
        if joke:
            st.subheader("A Little Joke:")
            st.write(joke)
