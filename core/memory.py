import streamlit as st


def get_history():
    return st.session_state.get("chat_history_text", "")


def update_history(question: str, sql: str):
    st.session_state.chat_history_text = (
        st.session_state.get("chat_history_text", "")
        + f"\nUser: {question}\nGenerated SQL: {sql}\n"
    )


def clear_history():
    st.session_state.chat_history_text = ""
    st.session_state.messages = []
