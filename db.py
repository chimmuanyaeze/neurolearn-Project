# db.py
import os
import logging
import streamlit as st
from st_supabase_connection import SupabaseConnection

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configure a console handler so errors are visible in deploy logs too
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


@st.cache_resource
def init_supabase(cache_buster: str | None = None):
    """
    Initialize and return a Supabase connection wrapper via Streamlit's st.connection.
    Raises RuntimeError on missing configuration.
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            logger.error("Supabase URL/KEY not set in environment variables.")
            raise RuntimeError("Supabase configuration missing. Please set SUPABASE_URL and SUPABASE_KEY.")

        # Use streamlit's connection factory for Supabase
        conn = st.connection(
            name="supabase",
            type=SupabaseConnection,
            url=supabase_url,
            key=supabase_key,
        )
        logger.info("Supabase connection initialized.")
        return conn

    except Exception as exc:
        logger.exception("Failed to initialize supabase connection.")
        # Re-raise so callers can handle (and Streamlit can stop if desired)
        raise
