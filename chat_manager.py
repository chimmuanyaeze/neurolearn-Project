# chat_manager.py
import streamlit as st
import uuid

def initialize_chat_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = []
    if "chat_titles" not in st.session_state:
        st.session_state.chat_titles = []
    if "current_chat_index" not in st.session_state:
        st.session_state.current_chat_index = None

def start_new_chat():
    st.session_state.current_chat = []
    st.session_state.current_chat_index = None

def save_current_chat_as_new(title=None):
    if not st.session_state.current_chat:
        return

    if not title:
        first_message = next((msg for msg in st.session_state.current_chat if msg['role'] == "user"), None)
        title = first_message['content'][:30] + ("..." if len(first_message['content']) > 30 else "") if first_message else "Untitled Chat"

    st.session_state.chat_titles.append(title)
    st.session_state.chat_history.append(st.session_state.current_chat[:])
    st.session_state.current_chat_index = len(st.session_state.chat_history) - 1

def select_chat(index):
    if 0 <= index < len(st.session_state.chat_history):
        st.session_state.current_chat = st.session_state.chat_history[index]
        st.session_state.current_chat_index = index

def append_to_current_chat(role, content_type, content):
    st.session_state.current_chat.append({
        "role": role,
        "type": content_type,
        "content": content
    })

def get_current_chat():
    return st.session_state.current_chat

def get_chat_titles():
    return st.session_state.chat_titles

def get_all_chats():
    return st.session_state.chat_history
