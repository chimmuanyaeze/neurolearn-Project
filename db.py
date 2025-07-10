# db.py
import streamlit as st
from st_supabase_connection import SupabaseConnection
import os

@st.cache_resource
# ADD A TEMPORARY PARAMETER TO BUST THE CACHE
def init_supabase(cache_buster=None):
    """
    Initializes and returns a SupabaseConnection object using environment variables.
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        # --- DEBUG PRINTS (KEEP THESE) ---
        print(f"DEBUG: init_supabase - Retrieved SUPABASE_URL: '{supabase_url}'")
        print(f"DEBUG: init_supabase - Retrieved SUPABASE_KEY (first 5 chars): '{supabase_key[:5]}'")
        # --- END DEBUG PRINTS ---

        if not supabase_url or not supabase_key:
            st.error("Supabase credentials (SUPABASE_URL, SUPABASE_KEY) are missing in environment variables. Please check your Render service's environment variable settings.")
            st.stop()

        return st.connection(
            name="supabase",
            type=SupabaseConnection,
            url=supabase_url,
            key=supabase_key,
        )
    except Exception as e:
        st.error(f"Error initializing Supabase connection: {e}")
        st.stop()