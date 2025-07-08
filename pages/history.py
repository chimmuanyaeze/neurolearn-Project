import streamlit as st
from chat_storage import get_chat_list, get_chat_by_id, delete_chat_by_id, rename_chat_by_id
from auth import get_current_user, logout
from datetime import datetime
import json
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="📖 Chat History - NeuroLearn", layout="wide")

# --- Auth ---
user = get_current_user()
if not user:
    st.warning("🔒 Please log in to view your chat history.")
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.title("🧾 History Navigation")
    st.markdown("View and manage previous STEM sessions.")

    if st.button("🚪 Logout"):
        logout()
        st.rerun()

    theme = st.toggle("🌗 Dark Mode", key="dark-mode-toggle")
    if theme:
        st.markdown("""
            <style>
                body { background-color: #121212; color: white; }
                .stButton>button { background-color: #333 !important; color: white !important; }
            </style>
        """, unsafe_allow_html=True)

# --- Header ---
st.title("📖 Your Saved Chats")

# --- Search Bar ---
search = st.text_input("🔍 Search chat titles...").lower()

# --- Chat List ---
chat_list = get_chat_list(user["id"])

if not chat_list:
    st.info("You have no saved chats yet.")
else:
    filtered_chats = [c for c in chat_list if search in c["title"].lower()]

    for chat in filtered_chats:
        chat_id = chat["id"]
        chat_title = chat["title"]
        created_at = chat.get("created_at")
        readable_time = datetime.fromisoformat(created_at).strftime("%Y-%m-%d %H:%M") if created_at else "Unknown time"

        with st.expander(f"📌 {chat_title} ({readable_time})"):
            messages = get_chat_by_id(chat_id)
            for msg in messages:
                avatar = "👤" if msg["role"] == "user" else "🤖"
                timestamp = msg.get("timestamp", readable_time)
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(f"{msg['content']}\n\n*⏱️ {timestamp}*") if msg["type"] == "text" else st.video(msg["content"])

            st.markdown("---")
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

            with col1:
                if st.button("🗑️ Delete", key=f"delete-{chat_id}"):
                    with st.modal(f"Are you sure you want to delete '{chat_title}'?"):
                        st.error("This action cannot be undone.")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("Yes, delete", key=f"confirm-delete-{chat_id}"):
                                delete_chat_by_id(chat_id)
                                st.success("Chat deleted.")
                                st.rerun()
                        with c2:
                            st.button("Cancel")

            with col2:
                new_title = st.text_input("✏️ Rename", value=chat_title, key=f"rename-{chat_id}")
                if st.button("💾 Save", key=f"save-rename-{chat_id}"):
                    rename_chat_by_id(chat_id, new_title)
                    st.success("Title updated.")
                    st.rerun()

            with col3:
                if st.button("🔁 Resume Chat", key=f"resume-{chat_id}"):
                    st.session_state.current_chat = messages
                    st.session_state.current_chat_id = chat_id
                    st.switch_page("app.py")

            with col4:
                export_format = st.radio("📤 Export As", ["JSON", "PDF"], key=f"format-{chat_id}", horizontal=True)
                if st.button("⬇️ Download", key=f"download-{chat_id}"):
                    if export_format == "JSON":
                        st.download_button(
                            label="Download JSON",
                            file_name=f"chat_{chat_id}.json",
                            mime="application/json",
                            data=json.dumps(messages, indent=2)
                        )
                    elif export_format == "PDF":
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        for m in messages:
                            role = m['role'].capitalize()
                            text = m['content'] if m['type'] == 'text' else f"[Video: {m['content']}]"
                            pdf.multi_cell(0, 10, f"{role}: {text}\n")
                        buffer = BytesIO()
                        pdf.output(buffer)
                        st.download_button(
                            label="Download PDF",
                            file_name=f"chat_{chat_id}.pdf",
                            mime="application/pdf",
                            data=buffer.getvalue()
                        )
