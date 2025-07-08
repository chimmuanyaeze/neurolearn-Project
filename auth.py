# auth.py
import streamlit as st
from streamlit_supabase_auth import login_form, logout_button

def show_login():
    try:
        session = login_form(
            url=st.secrets["auth"]["supabase"]["url"], # Correct access
            apiKey=st.secrets["auth"]["supabase"]["key"], # Correct access
            providers=["google", "github", "email"]
        )

        if session:
            st.session_state.user = session["user"]
            st.rerun() # Rerun after successful login to render main app content
        else:
            # If no session, app stops here to force login
            st.stop()

        return st.session_state.user # Return user from session_state for consistency
    except KeyError as e:
        # This error suggests an issue with how secrets are named/accessed by the library
        st.error(f"Configuration Error in auth.py: Missing secret '{e}'. "
                 "Please ensure .streamlit/secrets.toml has an [auth.supabase] section "
                 "with 'url' and 'key' defined (or 'auth' and 'supabase' nested if using dotted keys).")
        st.stop()

def get_current_user():
    return st.session_state.get("user")

def is_logged_in():
    return "user" in st.session_state and st.session_state.user is not None

def logout():
    # Attempt to clear the user session directly via the library if possible
    # streamlit_supabase_auth doesn't expose a direct logout function in the Python side
    # that also clears the browser's local storage/cookies.
    # The logout_button() widget in the sidebar usually handles the browser-side clear.

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

 
def get_remaining_uses():
    if "usage_count" not in st.session_state:
        st.session_state.usage_count = 0
    return max(0, 3 - st.session_state.usage_count)
    # Force a rerun to a clean state.
    # This crucial step forces Streamlit to re-evaluate without the old user in session_state.
    st.rerun() #