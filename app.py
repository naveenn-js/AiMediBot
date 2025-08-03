import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load environment variables ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ Google API Key not found. Please set it in the .env file.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# --- Set up Gemini Model ---
model = genai.GenerativeModel("gemini-1.5-flash-latest")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Flag to control clearing input
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Language selection
if "language" not in st.session_state:
    st.session_state.language = "English"

# --- Page Config ---
st.set_page_config(page_title="🧠 AI Mental Health Chat", layout="centered")

# --- Styling (Background) ---
def set_bg(image_path):
    with open(image_path, "rb") as img_file:
        img_data = img_file.read()
    import base64
    img_str = base64.b64encode(img_data).decode()
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{img_str}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .chat-msg {{
                background-color: rgba(0,0,0,0.5);
                color: white;
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
                white-space: pre-wrap;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

if os.path.exists("background.png"):
    set_bg("background.png")

# --- Language Selection ---
language_options = {
    "English": "Respond in English",
    "Hindi": "हिंदी में जवाब दें",
    "Malayalam": "മലയാളത്തിൽ മറുപടി നൽകുക",
    "Tamil": "தமிழில் பதிலளிக்கவும்"
}

st.session_state.language = st.selectbox(
    "🌐 Select Language",
    list(language_options.keys()),
    index=list(language_options.keys()).index(st.session_state.language)
)

# --- Display Title ---
st.markdown("## 🧘‍♂️ AI Mental Health Support")

# --- Display Chat History ---
for msg in st.session_state.chat.history:
    role = "🧑 You" if msg.role == "user" else "🤖 AI"
    text = msg.parts[0].text
    st.markdown(f"<div class='chat-msg'><b>{role}:</b> {text}</div>", unsafe_allow_html=True)

# --- User Input & Send Button ---
default_prompt = "" if st.session_state.clear_input else st.session_state.get("input", "")

col1, col2 = st.columns([5, 1])
with col1:
    prompt = st.text_input("💬", label_visibility="collapsed", key="input", value=default_prompt)
with col2:
    if st.button("📤 Send") and prompt:
        # Add language instruction to the prompt
        full_prompt = f"{prompt}\n\n{language_options[st.session_state.language]}"
        response = st.session_state.chat.send_message(full_prompt)
        st.session_state.clear_input = True  # Clear input on next rerun
        st.rerun()

# Reset clear_input flag after input cleared
if st.session_state.clear_input and prompt == "":
    st.session_state.clear_input = False

# --- Clear Chat Button ---
if st.button("🧹 Clear Chat"):
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.clear_input = True
    st.rerun()