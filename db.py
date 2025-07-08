# db.py
import streamlit as st
from st_supabase_connection import SupabaseConnection

@st.cache_resource
def init_supabase():
    """
    Initializes and returns a SupabaseConnection object using secrets.toml.
    """
    try:
        return st.connection(
            name="supabase",
            type=SupabaseConnection,
            # CORRECTED: Access using nested dictionary keys
            url=st.secrets["connections"]["supabase"]["SUPABASE_URL"],
            key=st.secrets["connections"]["supabase"]["SUPABASE_KEY"],
        )
    except KeyError as e:
        st.error(f"Configuration Error in db.py: Missing secret '{e}'. "
                 "Please ensure .streamlit/secrets.toml has a [connections.supabase] section "
                 "with 'SUPABASE_URL' and 'SUPABASE_KEY' defined.")
        st.stop()