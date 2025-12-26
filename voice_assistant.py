# -------------------------------
# 🎤 Voice Assistant using SpeechRecognition + pyttsx3 + pywhatkit
# -------------------------------

import speech_recognition as sr
import pyttsx3 as pt
import pywhatkit as pk

# -----------------------------------
# Initialize Recognizer and Speech Engine
# -----------------------------------
recognizer = sr.Recognizer()
engine = pt.init()

# -----------------------------------
# Text-to-Speech Function
# -----------------------------------
def speak(text):
    """Convert the given text to speech."""
    engine.say(text)
    engine.runAndWait()
    
# -----------------------------------
# Speech Recognition Function
# -----------------------------------
def hear():
    """
    Listen to user's voice command through microphone,
    convert it to text using Google Speech Recognition.
    """
    command = ""

    try:
        with sr.Microphone() as mic:
            print("🎧 Listening...")
            voice = recognizer.listen(mic)

            # Recognize speech using Google's API
            command = recognizer.recognize_google(voice)
            command = command.lower()

            # Check for wake word 'kodi'
            if 'shalu' in command:
                command = command.replace('shalu', '').strip()
                print(f"🗣️ Command after removing wake word: {command}")

    except Exception as e:
        print(f"⚠️ Error: {e}")
    return command


# -----------------------------------
# Command Processing Function
# -----------------------------------
def run():
    """Process the recognized command and perform actions."""
    command = hear()
    print(f"📥 Received command: {command}")

    if 'play' in command:
        song = command.replace('play', '').strip()
        speak(f"Playing {song}")
        pk.playonyt(song)  # Play the song on YouTube
    else:
        speak("Sorry, I didn't understand the command.")


# -----------------------------------
# Program Entry Point
# -----------------------------------
if __name__ == "__main__":
    run()
    engine.stop()  # ✅ Prevent pyttsx3 cleanup warning
