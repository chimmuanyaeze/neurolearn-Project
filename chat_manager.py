# chat_manager.py
import streamlit as st
import uuid
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Streamlit session-state key names used by the app
_CHAT_HISTORY_KEY = "chat_history"
_CURRENT_CHAT_KEY = "current_chat"
_CHAT_TITLES_KEY = "chat_titles"
_CURRENT_CHAT_INDEX_KEY = "current_chat_index"


def _ensure_state():
    """
    Ensure the session_state contains required keys.
    Safe to call on each import or operation.
    """
    if _CHAT_HISTORY_KEY not in st.session_state:
        st.session_state[_CHAT_HISTORY_KEY] = []
    if _CURRENT_CHAT_KEY not in st.session_state:
        st.session_state[_CURRENT_CHAT_KEY] = []
    if _CHAT_TITLES_KEY not in st.session_state:
        st.session_state[_CHAT_TITLES_KEY] = []
    if _CURRENT_CHAT_INDEX_KEY not in st.session_state:
        st.session_state[_CURRENT_CHAT_INDEX_KEY] = None


def initialize_chat_state():
    """
    Initialize session state for chat manager. Call this when app starts.
    """
    _ensure_state()
    logger.info("Initialized chat session state")


def start_new_chat():
    """
    Start a fresh chat in session state.
    """
    _ensure_state()
    st.session_state[_CURRENT_CHAT_KEY] = []
    st.session_state[_CURRENT_CHAT_INDEX_KEY] = None
    logger.info("Started new chat in session")


def save_current_chat_as_new(title: str | None = None) -> int:
    """
    Save the current chat in memory (session state) as a new chat.
    Returns the new index in chat_history.
    """
    _ensure_state()
    current = st.session_state.get(_CURRENT_CHAT_KEY, [])
    if not current:
        logger.warning("save_current_chat_as_new called with empty current chat — no-op")
        return -1

    if not title:
        # find first user message for title fallback
        first_user = next((m for m in current if m.get("role") == "user"), None)
        title = (first_user.get("content")[:30] + ("..." if len(first_user.get("content", "")) > 30 else "")) if first_user else "Untitled Chat"

    title_safe = title[:200]
    st.session_state[_CHAT_TITLES_KEY].append(title_safe)
    st.session_state[_CHAT_HISTORY_KEY].append(list(current))  # store a shallow copy
    st.session_state[_CURRENT_CHAT_INDEX_KEY] = len(st.session_state[_CHAT_HISTORY_KEY]) - 1
    logger.info("Saved current chat as new with title='%s' index=%s", title_safe, st.session_state[_CURRENT_CHAT_INDEX_KEY])
    return st.session_state[_CURRENT_CHAT_INDEX_KEY]


def select_chat(index: int) -> None:
    """
    Select a chat from session-based history by index.
    """
    _ensure_state()
    try:
        if index is None or not isinstance(index, int):
            raise ValueError("Index must be integer")
        if not (0 <= index < len(st.session_state[_CHAT_HISTORY_KEY])):
            raise IndexError("Index out of range")
        st.session_state[_CURRENT_CHAT_KEY] = list(st.session_state[_CHAT_HISTORY_KEY][index])  # copy
        st.session_state[_CURRENT_CHAT_INDEX_KEY] = index
        logger.info("Selected chat index=%s", index)
    except Exception:
        logger.exception("Failed to select chat index=%s", index)
        raise


def append_to_current_chat(role: str, content_type: str, content: Any) -> None:
    """
    Append a message to the current chat. Role must be 'user' or 'assistant' (validated).
    content_type should be 'text' or 'video' etc. Content is stored as-is, but
    text content is truncated to reasonable length to avoid session bloat.
    """
    _ensure_state()
    if role not in ("user", "assistant", "system"):
        logger.warning("append_to_current_chat called with unexpected role=%s", role)
        raise ValueError("Invalid role")

    content_type = (content_type or "text").lower()
    # Truncate text content so session_state doesn't grow unbounded
    if content_type == "text" and isinstance(content, str):
        content = content[:20000]

    message = {
        "id": str(uuid.uuid4()),
        "role": role,
        "type": content_type,
        "content": content
    }
    st.session_state[_CURRENT_CHAT_KEY].append(message)
    logger.debug("Appended message id=%s role=%s type=%s", message["id"], role, content_type)


def get_current_chat() -> List[Dict[str, Any]]:
    _ensure_state()
    # return direct reference for compatibility (previous code expects list)
    return st.session_state[_CURRENT_CHAT_KEY]


def get_chat_titles() -> List[str]:
    _ensure_state()
    return st.session_state[_CHAT_TITLES_KEY]


def get_all_chats() -> List[List[Dict[str, Any]]]:
    _ensure_state()
    return st.session_state[_CHAT_HISTORY_KEY]
