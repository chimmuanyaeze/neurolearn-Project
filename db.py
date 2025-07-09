# db.py
import streamlit as st
from st_supabase_connection import SupabaseConnection
import os # ADD THIS IMPORT

@st.cache_resource
def init_supabase():
    """
    Initializes and returns a SupabaseConnection object using environment variables.
    """
    try:
        # Fetch Supabase credentials directly from environment variables
        # These correspond to the SUPABASE_URL and SUPABASE_KEY you set in Render
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        # Add a check to ensure the environment variables are actually set
        if not supabase_url or not supabase_key:
            st.error("Supabase credentials (SUPABASE_URL, SUPABASE_KEY) are missing in environment variables. Please check your Render service's environment variable settings.")
            st.stop() # Stop the app if crucial credentials are not found

        return st.connection(
            name="supabase",
            type=SupabaseConnection,
            url=supabase_url, # Use the variable fetched from os.getenv()
            key=supabase_key, # Use the variable fetched from os.getenv()
        )
    except Exception as e: # Catch a broader exception for any potential issues during initialization
        st.error(f"Error initializing Supabase connection: {e}")
        st.stop()