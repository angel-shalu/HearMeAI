import streamlit as st
import importlib
import urllib.parse
import webbrowser
import os
import requests
from datetime import datetime
import asyncio
import inspect

# ---------- Async Safe Runner ----------
def run_async_safe(func, *args):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        future = asyncio.run_coroutine_threadsafe(func(*args), loop)
        return future.result()
    else:
        return asyncio.run(func(*args))

# ---------- Call sync or async safely ----------
def call_maybe_async(func, *args):
    if inspect.iscoroutinefunction(func):
        return run_async_safe(func, *args)
    else:
        return func(*args)

# ---------- Load assistant ----------
try:
    assistant = importlib.import_module("voice_assistant")
except Exception as e:
    st.error(f"Failed to import assistant module: {e}")
    st.stop()

st.set_page_config(page_title="Voice Assistant", page_icon="🎤", layout="centered")

# ---------------- Session ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ---------------- Sidebar ----------------
st.sidebar.title("⚙ Controls")

if st.sidebar.button("🌙 / ☀ Toggle Theme"):
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

enable_shutdown = st.sidebar.checkbox("Enable shutdown command", value=False)
volume = st.sidebar.slider("Volume (Windows)", 0, 100, 50)

# ---------------- Theme Fix ----------------
if st.session_state.theme == "light":
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f4f6f8, #e5ecf3, #dbe7f1) !important;
        color: #111 !important;
    }
    .glass {
        background: rgba(255,255,255,0.8) !important;
        color: #111 !important;
    }
    .title, .subtitle {
        color: #111 !important;
    }
    .chat-bubble {
        background: rgba(0,0,0,0.05) !important;
        color: #111 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- Custom CSS ----------
st.markdown("""
<style>

/* REMOVE STREAMLIT TOP BAR COMPLETELY */
[data-testid="stToolbar"] { display: none !important; }
header { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

.block-container { padding-top: 0rem !important; }

/* Background */
body { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }

/* Glass Card */
.glass {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 30px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    margin-top: 10px;
}

/* Title */
.title {
    font-size: 2.1rem;
    font-weight: 700;
    text-align: center;
    color: #ffffff;
    margin-bottom: 8px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #d1d1d1;
    margin-bottom: 25px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#00c6ff,#0072ff);
    border: none;
    border-radius: 14px;
    padding: 12px 24px;
    color: white;
    font-weight: 600;
    transition: 0.3s;
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 18px #00c6ff;
}

/* Chat bubble */
.chat-bubble {
    background: rgba(0,0,0,0.45);
    border-radius: 16px;
    padding: 15px 20px;
    margin-top: 15px;
    color: #ffffff;
    animation: fadeIn 0.5s ease-in;
}

/* Floating mic animation */
.mic {
    font-size: 3rem;
    text-align: center;
    animation: float 2.5s ease-in-out infinite;
    margin-bottom: 10px;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ---------- UI ----------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("<div class='mic'>🎤</div>", unsafe_allow_html=True)
st.markdown("<div class='title'>Smart Voice Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Speak commands like <i>Play song name</i></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("🎙 Listen", use_container_width=True):
        with st.spinner("Listening..."):
            try:
                cmd = call_maybe_async(assistant.hear)
            except Exception as e:
                st.error(f"Voice error: {e}")
                cmd = ""
        if cmd:
            st.session_state.chat.append(("user", cmd))
            st.session_state["cmd"] = cmd
            st.success("Voice captured!")
        else:
            st.warning("No voice detected.")

with col2:
    if st.button("🔊 Speak Back", use_container_width=True):
        text = st.session_state.get("cmd","")
        if text:
            call_maybe_async(assistant.speak, text)
        else:
            st.warning("Nothing to speak.")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- Command Logic ----------
def handle_command(cmd):
    c = cmd.lower()

    if c.startswith("play"):
        song = cmd[4:].strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(song)}")
        return f"Playing {song} 🎵"

    if c.startswith("open"):
        site = cmd.replace("open","").strip()
        webbrowser.open(f"https://{site}.com")
        return f"Opening {site}"

    if c.startswith("search"):
        q = cmd.replace("search","").strip()
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote_plus(q)}")
        return f"Searching for {q}"

    if "time" in c:
        return f"Time: {datetime.now().strftime('%H:%M')}"

    if "date" in c:
        return f"Date: {datetime.now().strftime('%d %B %Y')}"

    if c.startswith("weather"):
        city = cmd.replace("weather","").strip() or "Delhi"
        w = requests.get(f"https://wttr.in/{city}?format=3").text
        return f"🌤 {w}"

    if c.startswith("volume"):
        os.system(f"nircmd.exe setsysvolume {volume*655}")
        return f"Volume set to {volume}%"

    if "shutdown" in c and enable_shutdown:
        os.system("shutdown /s /t 5")
        return "Shutting down system..."

    return "Sorry, I didn't understand."

# ---------- Transcript + Chat ----------
cmd = st.session_state.get("cmd","")

if cmd:
    reply = handle_command(cmd)
    st.session_state.chat.append(("bot", reply))
    call_maybe_async(assistant.speak, reply)
    st.session_state["cmd"] = ""

st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("### 💬 Chat History")
for role,msg in st.session_state.chat:
    st.markdown(f"<div class='chat-bubble'>{msg}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.caption("⚠ Run locally for microphone & system commands.")
st.caption("Developed by OpenAI ChatGPT")
