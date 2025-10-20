# app.py (production-ready)
import os
import logging
import time
import threading
import queue
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import uuid

# Local imports (ensure visuals/generator.py exists and exposes the functions)
from chains.solution_chain import get_solution
import visuals.generator as gen  # import module to access run_with_retries & functions
from chat_manager import (
    initialize_chat_state, start_new_chat, save_current_chat_as_new,
    append_to_current_chat, get_current_chat
)
from auth import show_login, is_logged_in, logout, get_remaining_uses, get_current_user
from db import init_supabase
from chat_storage import get_chat_list, save_chat, get_chat_by_id

# ----------------------
# Load env and basic checks
# ----------------------
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# ----------------------
# Logging
# ----------------------
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_dir / "app.log",
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.info("App start")

# ----------------------
# Streamlit config
# ----------------------
st.set_page_config(
    page_title="NeuroLearn STEM Visualizer",
    page_icon="favicon.ico",
    layout="wide"
)

# ----------------------
# Initialize app-state & DB
# ----------------------
initialize_chat_state()
supabase = init_supabase(cache_buster="version_1")
user = get_current_user()

# Create a base media directory (can be changed per deployment)
BASE_MEDIA_DIR = Path(os.getenv("BASE_MEDIA_DIR", "/tmp/media"))
BASE_MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------
# Sidebar (chats + login)
# ----------------------
with st.sidebar:
    st.markdown("### My Chats")
    if user:
        try:
            chat_list = get_chat_list(user["id"])
        except Exception as e:
            logger.exception("Failed to fetch chat list")
            chat_list = []
        for chat in chat_list:
            if st.button(chat["title"], key=f"chat-{chat['id']}"):
                try:
                    st.session_state.current_chat = get_chat_by_id(chat["id"])
                except Exception as e:
                    logger.exception("Failed to load chat by id: %s", chat["id"])
                    st.error("Failed to load chat.")
                st.rerun()

    if st.button("Start New Chat"):
        start_new_chat()
        st.rerun()

    # Theme toggle (simple)
    theme_toggle = st.checkbox("Dark Mode", key="theme_toggle")
    if theme_toggle:
        st.markdown('<style>body { background-color: #121212; color: white; }</style>', unsafe_allow_html=True)

    st.markdown("---")

    if user:
        st.success(f"{user.get('email')} (Logged in)")
        if st.button("Logout"):
            logout()
    else:
        st.info(f"You have {get_remaining_uses()} free uses left.")
        show_login()

# ----------------------
# App Title
# ----------------------
st.title("NeuroLearn STEM Tutor")
st.caption("Chat with an AI tutor and receive video-based STEM explanations.")

# ----------------------
# Cancel button / state
# ----------------------
if "cancel_flag" not in st.session_state:
    st.session_state.cancel_flag = False

def set_cancel_flag():
    st.session_state.cancel_flag = True

# Use separate cancel button so user can press during long tasks
st.sidebar.button("Cancel Current Task", on_click=set_cancel_flag)

# Reset cancel flag helper
def reset_cancel_flag():
    st.session_state.cancel_flag = False

# ----------------------
# Utilities: per-user media dir
# ----------------------
def get_media_dir_for_user(user_obj):
    """
    Return a Path object for user-specific media directory.
    If user_obj is None, fallback to session-based directory.
    """
    if user_obj and user_obj.get("id"):
        user_id = str(user_obj["id"])
    else:
        # Use Streamlit session id if available, or a generated UUID per session
        user_id = st.session_state.get("session_id") or str(uuid.uuid4())
        st.session_state["session_id"] = user_id
    user_media = BASE_MEDIA_DIR / user_id
    user_media.mkdir(parents=True, exist_ok=True)
    return user_media

# ----------------------
# Helper: threaded runner with progress callback
# ----------------------
def run_task_in_thread(task_fn, description):
    """
    Runs a task function in a worker thread and updates Streamlit UI
    using a progress_callback accepted by the task (progress, eta).
    task_fn must accept a progress_callback function.
    Returns the task result or raises the exception.
    Respects st.session_state.cancel_flag to cancel waiting and abort subsequent steps.
    """
    progress_bar = st.progress(0.0)
    status = st.empty()
    result_q = queue.Queue()

    def progress_callback(progress_fraction, eta_seconds=None):
        """This callback is passed to generator functions."""
        try:
            p = min(max(progress_fraction, 0.0), 1.0)
            progress_bar.progress(p)
            eta_text = f" — ETA: {int(eta_seconds)}s" if eta_seconds is not None else ""
            status.text(f"{description}{eta_text}")
        except Exception:
            # UI update failures should not crash worker thread
            logger.exception("Progress callback UI update failed")

    def worker():
        try:
            result = task_fn(progress_callback)
            result_q.put(("ok", result))
        except Exception as e:
            logger.exception("Task failed: %s", description)
            result_q.put(("err", e))

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    # Wait loop: allow streaming progress via callbacks and handle cancellation
    while True:
        if st.session_state.cancel_flag:
            # Mark cancelled and return None to indicate cancellation
            logger.info("User requested cancellation for task: %s", description)
            # Reset the cancel flag to allow future runs
            reset_cancel_flag()
            status.text("Cancelled")
            progress_bar.empty()
            return None
        # If thread finished, fetch result
        if not thread.is_alive():
            break
        # Let the progress callbacks update the UI (they do asynchronously)
        time.sleep(0.25)

    # Get worker result
    try:
        status_val, payload = result_q.get_nowait()
    except queue.Empty:
        # No result placed: treat as failure
        raise RuntimeError("Task thread finished without result")

    if status_val == "err":
        raise payload
    # Ensure final progress is displayed
    progress_bar.progress(1.0)
    status.text(f"{description} — complete")
    return payload

# ----------------------
# Chat input & pipeline
# ----------------------
if is_logged_in() or get_remaining_uses() > 0:
    query = st.chat_input("Enter your STEM problem here...")
    if query:
        # track usage if not logged in
        if not is_logged_in():
            st.session_state.usage_count = st.session_state.get("usage_count", 0) + 1

        with st.chat_message("user"):
            st.markdown(query)

        try:
            # 1) Generate solution object (retries inside if desired)
            with st.spinner("Generating solution..."):
                sol = gen.run_with_retries(lambda: get_solution(query), retries=3, wait=2)
                logger.info("Solution generated for query (truncated): %s", query[:120])

            # Prepare per-user media dir
            user_media_dir = get_media_dir_for_user(user)

            # 2) Generate video (with live progress + ETA)
            video_name = f"solution_{uuid.uuid4().hex[:10]}"
            def video_task(progress_cb):
                return gen.generate_full_solution_video(
                    sol,
                    video_name,
                    resolution="720p",
                    progress_callback=progress_cb,
                    media_dir=user_media_dir
                )
            video_path = run_task_in_thread(lambda cb: gen.run_with_retries(video_task, retries=3, wait=3, **{"progress_callback": cb}), "Generating video")
            if video_path is None:
                st.warning("Video generation cancelled by user.")
                raise RuntimeError("Video generation cancelled")

            # 3) Generate TTS (with progress)
            tts_name = f"tts_{uuid.uuid4().hex[:10]}"
            def tts_task(progress_cb):
                return gen.generate_tts_audio(sol, tts_name, media_dir=user_media_dir, progress_callback=progress_cb)
            audio_path = run_task_in_thread(lambda cb: gen.run_with_retries(tts_task, retries=3, wait=2, **{"progress_callback": cb}), "Generating narration")
            if audio_path is None:
                st.warning("Audio generation cancelled by user.")
                raise RuntimeError("Audio generation cancelled")

            # 4) Merge audio & video (short operation, still wrapped for retries)
            merge_name = f"final_{uuid.uuid4().hex[:8]}"
            def merge_task(_progress_cb):
                return gen.merge_audio_video(video_path, audio_path, merge_name, media_dir=user_media_dir)
            final_path = gen.run_with_retries(lambda: merge_task(None), retries=2, wait=2)
            logger.info("Final video created: %s", final_path)

            # 5) Append to chat and save
            append_to_current_chat("user", "text", query)
            append_to_current_chat("assistant", "text", f"Restated Problem: {sol.get('problem', '')}")
            for step in sol.get("steps", []):
                append_to_current_chat("assistant", "text", f"{step.get('title', '')}\n{step.get('explanation', '')}")
            append_to_current_chat("assistant", "video", str(final_path))

            # Persist chat session in memory & DB
            save_current_chat_as_new(query[:30] + ("..." if len(query) > 30 else ""))
            if user:
                try:
                    save_chat(user["id"], query[:30], get_current_chat())
                except Exception:
                    logger.exception("Failed to save chat to DB")

            # Re-run to show results
            st.rerun()

        except Exception as exc:
            logger.exception("Error during pipeline")
            st.error(f"Error: {exc}")
else:
    st.info("Please log in or use a free attempt to start chatting.")

# ----------------------
# Display current chat
# ----------------------
if get_current_chat():
    for msg in get_current_chat():
        with st.chat_message(msg["role"]):
            if msg["type"] == "text":
                st.markdown(msg["content"])
            elif msg["type"] == "video":
                try:
                    st.video(msg["content"])
                except Exception:
                    logger.exception("Failed to display video: %s", msg["content"])
                    st.write("Video available at:", msg["content"])
