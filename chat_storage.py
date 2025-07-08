import json
from db import init_supabase

def get_chat_list(user_id):
    supabase = init_supabase()
    result = (
    supabase
    .table("chats")
    .select("id, title, created_at")
    .eq("user_id", user_id)
    .order("created_at", desc=True)
    .execute()
)
    return result.data if result and result.data else []

def get_chat_by_id(chat_id):
    supabase = init_supabase()
    result = supabase.execute_query(
        f"SELECT messages FROM chats WHERE id = '{chat_id}'"
    )
    return json.loads(result.data[0]["messages"]) if result and result.data else []

def save_chat(user_id, title, messages):
    supabase = init_supabase()
    supabase.execute_query(
        "INSERT INTO chats (user_id, title, messages) VALUES (%s, %s, %s)",
        [user_id, title, json.dumps(messages)]
    )

def delete_chat_by_id(chat_id):
    supabase = init_supabase()
    supabase.execute_query(
        f"DELETE FROM chats WHERE id = '{chat_id}'"
    )

def rename_chat_by_id(chat_id, new_title):
    supabase = init_supabase()
    supabase.execute_query(
        f"UPDATE chats SET title = %s WHERE id = %s",
        [new_title, chat_id]
    )

def resume_chat(chat_id):
    return get_chat_by_id(chat_id)
