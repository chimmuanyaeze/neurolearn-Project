# auth.py
import streamlit as st
from streamlit_supabase_auth import login_form, logout_button
import os # Import os module to access environment variables

def show_login():
    try:
        # Get credentials directly from environment variables
        # Use distinct names to avoid clashes with other Supabase variables
        auth_url = os.getenv("AUTH_SUPABASE_URL")
        auth_key = os.getenv("AUTH_SUPABASE_KEY")

        if not auth_url or not auth_key:
            st.error("Authentication configuration missing. Please ensure AUTH_SUPABASE_URL and AUTH_SUPABASE_KEY are set as environment variables.")
            st.stop()

        session = login_form(
            url=auth_url,
            apiKey=auth_key,
            providers=["google", "github", "email"]
        )

        if session:
            st.session_state.user = session["user"]
            st.rerun() # Rerun after successful login to render main app content
        else:
            # If no session, app stops here to force login
            st.stop()

        return st.session_state.user # Return user from session_state for consistency
    except Exception as e: # Catch a broader exception since KeyError is specific to st.secrets
        st.error(f"Error during login form initialization: {e}")
        st.stop()


def get_current_user():
    return st.session_state.get("user")

def is_logged_in():
    return "user" in st.session_state and st.session_state.user is not None

def logout():
    # Clear Streamlit's internal session state for the user
    if "user" in st.session_state:
        del st.session_state.user
    # Optionally, clear other chat-related states if you want a completely fresh start
    if "current_chat" in st.session_state:
        del st.session_state.current_chat
    if "chat_history" in st.session_state:
        del st.session_state.chat_history
    if "usage_count" in st.session_state:
        del st.session_state.usage_count

    # Force a rerun to a clean state.
    # This crucial step forces Streamlit to re-evaluate without the old user in session_state.
    st.rerun() # This line was already present in your original code


def get_remaining_uses():
    if "usage_count" not in st.session_state:
        st.session_state.usage_count = 0
    return max(0, 3 - st.session_state.usage_count)