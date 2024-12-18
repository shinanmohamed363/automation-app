import os
from openai import OpenAI
import speech_recognition as sr
import pyttsx3 
import logging
import datetime

# Initialize pyttsx3 engine for text-to-speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Set voice (use voices[0].id for male voice)

def speak(text):
    """This function converts text to speech"""
    engine.say(text)
    engine.runAndWait() 

def takecommand():
    """This function listens to the microphone and converts speech to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")

    except Exception as e:
        logging.info(e)
        print("Say that again please")
        speak("Say that again please")
        return "None"
    
    return query



# Set up the OpenAI client (ensure correct import and client initialization)
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def get_openai_response(query):
    """This function takes the user's command as input and gets a response from the OpenAI model."""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": query,
            },
        ],
        model="gpt-4o-mini",  # Ensure this model is available and correct
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0,
    )

    return response.choices[0].message.content

# Main program flow
if __name__ == "__main__":
    while True:
        # Take command from user
        command = takecommand().lower()

        # Special commands for Jarvis
        if "hey jarvis" in command:
            speak("Hey boss, I am online!")
            continue

        elif "boss" in command:
            speak("My boss's name is Shinan. He is always in front of the computer to update me.")
            continue

        elif "tell me a joke" in command:
            joke = "Why don't programmers like nature? It has too many bugs!"
            speak(joke)
            continue

        # Exit command
        elif "exit" in command:
            speak("Goodbye!")
            break
        
        # Send the command to OpenAI API and get the response
        if command != "None":
            response = get_openai_response(command)
            print(f"Response: {response}")
            speak(response)
