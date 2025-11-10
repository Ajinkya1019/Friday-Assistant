# Friday.py
# Voice-controlled personal assistant for PC
# Developed for local use with basic security

import pyttsx3
import speech_recognition as sr
import pywhatkit
import webbrowser
import datetime
import os
import sys

# --------------------------
# 1. TEXT-TO-SPEECH
# --------------------------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(voice.id) # See all available voices
engine.setProperty('voice', voices[1].id)  # Choose better voice
engine.setProperty('rate', 180)  # Slower = more natural 

def speak(text):
    print(f"FRIDAY: {text}")
    engine.say(text)
    engine.runAndWait()

# --------------------------
# 2. COMMAND PROCESSOR
# --------------------------
def process_command(cmd):
    cmd = cmd.lower()

    if "time" in cmd or "date" in cmd:
        now = datetime.datetime.now()
        full_time = now.strftime("%A, %d %B %Y, %H:%M hours")
        speak(f"It is {full_time}")

    elif "open whatsapp" in cmd:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")

    elif "open browser" in cmd:
        speak("Opening browser")
        webbrowser.open("https://www.google.com")

    elif "mute" in cmd:
        speak("Shutting down now.")
        sys.exit()

    else:
        speak("I don't understand that command.")

# --------------------------
# 3. VOICE AUTHENTICATION
# --------------------------
AUTH_PHRASE = "hello friday"  # change to your phrase

def listen_and_authenticate():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for auth phrase...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
        if AUTH_PHRASE in command:
            speak("Yes, sir?")
            return True
        else:
            speak("Access denied.")
            return False
    except sr.UnknownValueError:
        speak("I did not understand that.")
        return False

# --------------------------
# 4. MAIN LOOP
# --------------------------
if __name__ == "__main__":
    speak("Friday activated.")
    while True:
        if listen_and_authenticate():
            speak("What should I do?")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                cmd = r.recognize_google(audio).lower()
                process_command(cmd)
            except sr.UnknownValueError:
                speak("I did not understand the command.")
