import os
from datetime import datetime

import streamlit as st
from supabase import create_client


def _get_secret(name: str):
    return os.getenv(name) or st.secrets.get(name, None)


def _supabase_available():
    return bool(_get_secret("SUPABASE_URL") and _get_secret("SUPABASE_ANON_KEY"))


def _client():
    return create_client(_get_secret("SUPABASE_URL"), _get_secret("SUPABASE_ANON_KEY"))


def log_query(email, question, sql, success, exec_time, rows, error=""):
    record = {
        "email": email,
        "question": question,
        "sql": sql,
        "success": success,
        "execution_time": exec_time,
        "rows": rows,
        "error": error,
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

    if "query_logs" not in st.session_state:
        st.session_state.query_logs = []

    st.session_state.query_logs.append(record)

    if _supabase_available():
        try:
            _client().table("query_logs").insert(record).execute()
        except Exception:
            pass


def fetch_user_logs(email):
    if not _supabase_available():
        return st.session_state.get("query_logs", [])

    try:
        result = (
            _client()
            .table("query_logs")
            .select("*")
            .eq("email", email)
            .order("created_at", desc=True)
            .limit(200)
            .execute()
        )
        return result.data or []
    except Exception:
        return st.session_state.get("query_logs", [])


def clear_session_logs():
    st.session_state.query_logs = []
