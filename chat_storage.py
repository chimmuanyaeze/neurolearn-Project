# chat_storage.py
import json
import logging
import re
from typing import List, Dict, Any, Optional
from db import init_supabase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Basic UUID regex (loose) for validation of chat IDs
_UUID_RE = re.compile(r"^[0-9a-fA-F-]{8,36}$")


def _is_valid_chat_id(chat_id: str) -> bool:
    if not isinstance(chat_id, str):
        return False
    return bool(_UUID_RE.match(chat_id))


def _truncate_text(s: str, max_len: int = 10000) -> str:
    if not isinstance(s, str):
        s = str(s)
    return s[:max_len]


def get_chat_list(user_id: str) -> List[Dict[str, Any]]:
    """
    Returns a list of chats for a user ordered by created_at desc.
    Each entry includes id, title and created_at.
    """
    try:
        supabase = init_supabase()
        resp = (
            supabase
            .table("chats")
            .select("id,title,created_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        if resp and getattr(resp, "data", None) is not None:
            return resp.data
        return []
    except Exception as e:
        logger.exception("Error fetching chat list for user_id=%s", user_id)
        return []


def get_chat_by_id(chat_id: str) -> List[Dict[str, Any]]:
    """
    Fetch the messages (JSON) field for a single chat by id.
    Returns an empty list if not found.
    """
    if not _is_valid_chat_id(chat_id):
        raise ValueError("Invalid chat_id format.")

    try:
        supabase = init_supabase()
        resp = (
            supabase
            .table("chats")
            .select("messages")
            .eq("id", chat_id)
            .limit(1)
            .execute()
        )
        if resp and getattr(resp, "data", None):
            row = resp.data[0]
            # messages field could already be JSON; handle both cases
            messages = row.get("messages", "[]")
            if isinstance(messages, str):
                try:
                    return json.loads(messages)
                except Exception:
                    logger.warning("messages field not valid JSON for chat_id=%s", chat_id)
                    return []
            return messages
        return []
    except Exception:
        logger.exception("Failed to fetch chat by id: %s", chat_id)
        raise


def save_chat(user_id: str, title: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Insert a new chat row. Title and messages are sanitized/truncated.
    Returns the inserted row response.
    """
    title_safe = _truncate_text(title or "Untitled Chat", max_len=200)
    messages_json = json.dumps(messages, ensure_ascii=False)

    try:
        supabase = init_supabase()
        resp = (
            supabase
            .table("chats")
            .insert({
                "user_id": user_id,
                "title": title_safe,
                "messages": messages_json
            })
            .execute()
        )
        # The Supabase client returns .data on success
        return resp.data[0] if resp and getattr(resp, "data", None) else {}
    except Exception:
        logger.exception("Failed to save chat for user_id=%s title=%s", user_id, title_safe)
        raise


def delete_chat_by_id(chat_id: str) -> None:
    """
    Delete a chat by id using parameterized table delete.
    """
    if not _is_valid_chat_id(chat_id):
        raise ValueError("Invalid chat_id format.")

    try:
        supabase = init_supabase()
        supabase.table("chats").delete().eq("id", chat_id).execute()
        logger.info("Deleted chat id=%s", chat_id)
    except Exception:
        logger.exception("Failed to delete chat id=%s", chat_id)
        raise


def rename_chat_by_id(chat_id: str, new_title: str) -> None:
    """
    Rename a chat using an update call and parameterized input.
    """
    if not _is_valid_chat_id(chat_id):
        raise ValueError("Invalid chat_id format.")
    new_title_safe = _truncate_text(new_title or "Untitled Chat", max_len=200)

    try:
        supabase = init_supabase()
        supabase.table("chats").update({"title": new_title_safe}).eq("id", chat_id).execute()
        logger.info("Renamed chat id=%s to %s", chat_id, new_title_safe)
    except Exception:
        logger.exception("Failed to rename chat id=%s", chat_id)
        raise


def resume_chat(chat_id: str) -> List[Dict[str, Any]]:
    """
    Alias to get_chat_by_id for clarity.
    """
    return get_chat_by_id(chat_id)
