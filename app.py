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


st.set_page_config(page_title="📚 NeuroLearn STEM Visualizer", layout="wide")


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
st.title("🍯Bumble bee")
st.caption("Chat with an AI tutor and receive video-based explanations.")

# --- Render Chat Input and Process Query ---
# This entire block will only execute if show_login() *does NOT* call st.stop().
# i.e., when the user is logged in or if the login_form allows passage (e.g., free uses).
if is_logged_in() or get_remaining_uses() > 0: # Only show chat input if logged in or has free uses
    query = st.chat_input("Enter your STEM problem...")

    if query:
        if not is_logged_in(): # For free usage tracking
            st.session_state.usage_count += 1

        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("Thinking..."):
            try:
                sol = get_solution(query)
                video_name = "solution_" + str(uuid.uuid4())[:8]
                video_path = generate_full_solution_video(sol, video_name)
                audio_path = generate_tts_audio(sol, video_name)
                final_path = merge_audio_video(video_path, audio_path, video_name)

                append_to_current_chat("user", "text", query)
                append_to_current_chat("assistant", "text", f"**Restated Problem:** {sol['problem']}")
                for step in sol["steps"]:
                    append_to_current_chat("assistant", "text", f"**{step['title']}**\n{step['explanation']}")
                append_to_current_chat("assistant", "video", str(final_path))

                save_current_chat_as_new(query[:30] + ("..." if len(query) > 30 else ""))

                if user:
                    save_chat(user["id"], query[:30], get_current_chat())

                st.rerun()

            except Exception as e:
                st.error(f"❌ Error during solution generation: {e}")
else:
    # This else block means user is NOT logged in AND has no free uses
    st.info("Please log in or use your free attempts to start chatting.")


# --- Display Current Chat Messages (always show the current chat history) ---
# This block runs on every script execution to display the current_chat from session_state
if get_current_chat():
    for msg in get_current_chat():
        with st.chat_message(msg["role"]):
            if msg["type"] == "text":
                st.markdown(msg["content"])
            elif msg["type"] == "video":
                st.video(msg["content"])