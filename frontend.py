import streamlit as st
import speech_recognition as sr
import pyttsx3 as pt
import pywhatkit as pk
import time

# Streamlit page setup
st.set_page_config(page_title="🎧 Ak Voice Assistant", page_icon="🎤", layout="centered")

# Updated Styles
st.markdown("""
    <style>
        /* Hide the default Streamlit header space */
        header {visibility: hidden;}
        footer {visibility: hidden;}

        /* Background gradient */
        body {
            background: radial-gradient(circle at top left, #3b82f6, #9333ea, #111827);
        }

        /* Main container card */
        .main {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 25px;
            padding: 50px;
            margin: 40px auto;
            max-width: 700px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            backdrop-filter: blur(20px);
        }

        /* Title styling */
        .title {
            text-align: center;
            font-size: 48px;
            font-weight: 900;
            color: #e0e7ff;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        }

        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #cbd5e1;
            margin-bottom: 30px;
        }

        /* Input field styling */
        .stTextInput>div>div>input {
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            border-radius: 10px;
            border: 2px solid #60a5fa;
            font-size: 16px;
            padding: 10px;
        }
        .stTextInput>div>div>input::placeholder {
            color: #cbd5e1;
        }

        /* Button style */
        .stButton>button {
            background: linear-gradient(90deg, #2563eb, #9333ea);
            color: white;
            border-radius: 10px;
            border: none;
            padding: 12px 35px;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #1d4ed8, #7e22ce);
        }

        /* Mic animation */
        .mic {
            display: flex;
            justify-content: center;
            margin: 40px 0;
        }
        .pulse {
            width: 100px;
            height: 100px;
            background: #2563eb;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
            70% { box-shadow: 0 0 0 30px rgba(59, 130, 246, 0); }
            100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
        }
    </style>
""", unsafe_allow_html=True)


# Container start
st.markdown("<div class='main'>", unsafe_allow_html=True)

# Titles
st.markdown("<div class='title'>🎧 Voice Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask your favourite playlist or type below 🎵</div>", unsafe_allow_html=True)

# Voice type selection
voice_choice = st.radio("Choose Voice Type:", ("Male", "Female"), horizontal=True)

# Speak function with isolated engine
def speak(text):
    local_engine = pt.init()
    voices = local_engine.getProperty('voices')
    if voice_choice == 'Male':
        local_engine.setProperty('voice', voices[0].id)
    else:
        local_engine.setProperty('voice', voices[1].id)
    local_engine.say(text)
    local_engine.runAndWait()
    local_engine.stop()

# Speech recognition
recognizer = sr.Recognizer()

def hear():
    cmd = ""
    try:
        with sr.Microphone() as mic:
            st.info("Listening... Speak now")
            audio = recognizer.listen(mic, timeout=5)
            st.success("Got your voice! Processing...")
            cmd = recognizer.recognize_google(audio)
            cmd = cmd.lower()
            if "ak" in cmd:
                cmd = cmd.replace("ak", "").strip()
    except Exception as e:
        st.error(f" Error: {e}")
    return cmd

# Run assistant
def run(cmd):
    if cmd:
        st.write(f"You said: **{cmd}**")
        if "play" in cmd:
            song = cmd.replace("play", "").strip()
            speak(f"Playing {song}")
            st.success(f"🎵 Playing: {song}")
            time.sleep(1)
            pk.playonyt(song)
        else:
            speak("Sorry, I didn't understand the command.")
            st.warning("Command not recognized.")
    else:
        st.warning("No command detected. Try again!")

# Mic animation
st.markdown("<div class='mic'><div class='pulse'></div></div>", unsafe_allow_html=True)

# Input options
col1, col2 = st.columns(2)

with col1:
    if st.button("Speak Playlist"):
        user_cmd = hear()
        run(user_cmd)

with col2:
    user_input = st.text_input("Type your playlist here:")
    if st.button("Click to Play"):
        run(user_input.lower())

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; margin-top: 20px; color: #6b7280;'>Developed by Aneel Kumar M (AK)</div>", unsafe_allow_html=True)