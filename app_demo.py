import os
from dotenv import load_dotenv # Ensure .env is loaded to access environment variables when running locally
import streamlit as st
from chains.solution_chain import get_solution
from visuals.generator import generate_full_solution_video, generate_tts_audio, merge_audio_video
from pathlib import Path
import uuid
from chat_manager import (
    initialize_chat_state, start_new_chat, save_current_chat_as_new,
    select_chat, append_to_current_chat, get_current_chat, get_chat_titles
)
from auth import show_login, is_logged_in, logout, get_remaining_uses, get_current_user
from db import init_supabase
from chat_storage import get_chat_list, save_chat, get_chat_by_id

load_dotenv() # Ensure .env is loaded to access environment variables when running locally 

# This is a debugg  line that ensures the required environment variable is present
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Set the page title and icon
st.set_page_config(
    page_title="Bumblebee Project", # You can customize the title here
    page_icon="favicon.ico"
)


st.set_page_config(page_title=" NeuroLearn STEM Visualizer", layout="wide")


# --- Initialize State ---
initialize_chat_state()
supabase = init_supabase(cache_buster="version_1")
user = get_current_user()


# --- Sidebar: Chat Drawer & Login Controls ---
with st.sidebar:
    st.markdown("### 💬 My Chats")

    # If logged in, show chat list
    if user:
        # Assuming get_chat_list and get_chat_by_id internally use the globally initialized supabase from chat_storage.py
        chat_list = get_chat_list(user["id"])
        for chat in chat_list:
            if st.button(chat["title"], key=f"chat-{chat['id']}"):
                st.session_state.current_chat = get_chat_by_id(chat["id"])
                st.rerun()

    if st.button("➕ Start New Chat"):
        start_new_chat()
        st.rerun()

    theme = st.toggle("🌗 Dark Mode")
    if theme:
        st.markdown('<style>body { background-color: #121212; color: white; }</style>', unsafe_allow_html=True)

    st.markdown("---")
    # Login/Logout display logic
    if user:
        st.success(f"🔓 {user['email']}")
        if st.button("🚪 Logout"):
            logout()
    else:
        st.warning(f"🔒 You have {get_remaining_uses()} free uses left.")
        # show_login() will display the login form or stop the app.
        # This is correct placement for a login wall.
        show_login()


# --- App Title (always visible) ---
st.title("Neurolearn")
st.caption("Chat with an AI tutor and receive video-based explanations.")

# --- Render Chat Input and Process Query ---
# --- Render Chat Input and Process Query ---
# This entire block will only execute if the user is logged in or has free uses.
if is_logged_in() or get_remaining_uses() > 0: # Only show chat input if logged in or has free uses
    query = st.chat_input("Enter your STEM problem...")

    if query:
        if not is_logged_in(): # For free usage tracking
            st.session_state.usage_count += 1

        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("Preparing your demo..."):
            try:
                # --- DEMO LOGIC START ---
                # Instead of generating a solution, we will show a demo video and an explanation.

                demo_video_path = "assets/demo.mp4" # Path to your demo video

                # Professional explanation for the user
                explanation_message = """
                Thank you for your interest in the Neurolearn Project! Below is a demonstration video showcasing the type of high-quality, animated solution our platform generates.

                ### Why a Demo Version?
                While our core technology is fully functional, this demo is currently in place due to funding constraints for two essential, high-cost services:

                * **   OpenAI API Subscription:** Generating tailored, step-by-step solutions for each unique problem requires a paid subscription to powerful AI models.
                * **   High-Performance Hosting:** The video rendering process, powered by Manim, is computationally intensive and requires significant server RAM. To ensure fast video creation, a premium hosting plan is necessary.

                ### The Vision & Potential
                We are actively seeking funding to launch the full version, which we believe is a game-changer for STEM education.

                * ** Scalable:** Our architecture is built to handle a large volume of users and a vast range of academic subjects.
                * ** Innovative:** We solve a key problem for students who can't find tutorials for their specific questions. Our AI tutor creates bespoke video lessons on demand.
                * ** Profitable & Affordable:** The final product will be offered as an affordable subscription, creating a sustainable business while remaining accessible to students everywhere.

                We appreciate your understanding and hope this demo excites you about the future of personalized learning!
                """

                # Append user message, the explanation, and the demo video to the chat
                append_to_current_chat("user", "text", query)
                append_to_current_chat("assistant", "text", explanation_message)
                append_to_current_chat("assistant", "video", demo_video_path)

                # Save the chat session to maintain user history
                save_current_chat_as_new(query[:30] + ("..." if len(query) > 30 else ""))
                if user:
                    save_chat(user["id"], "DEMO - " + query[:24], get_current_chat())

                st.rerun()
                # --- DEMO LOGIC END ---

            except FileNotFoundError:
                st.error("❌ **Critical Error:** `assets/demo.mp4` not found. Please ensure the folder and video file exist.")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")
else:
    # This else block means user is NOT logged in AND has no free uses
    st.info("Please log in or sign up to start chatting.")


# --- Display Current Chat Messages (always show the current chat history) ---
# This block runs on every script execution to display the current_chat from session_state
if get_current_chat():
    for msg in get_current_chat():
        with st.chat_message(msg["role"]):
            if msg["type"] == "text":
                st.markdown(msg["content"])
            elif msg["type"] == "video":
                # Add a check for the video file's existence before trying to display it
                try:
                    st.video(msg["content"])
                except Exception:
                    st.error(f"Could not load video: {msg['content']}")


