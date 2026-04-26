import streamlit as st
import pandas as pd
from sqlalchemy import text
from db import get_engine, get_schema
from llm import generate_sql, fix_sql
from utils import is_safe, clean_sql

st.set_page_config(page_title="Text-to-SQL AI", layout="wide")
st.title("🧠 AI Data Analyst")

engine = get_engine()
schema = get_schema(engine)

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.chat_input("Ask your data question...")

if user_input:
    st.session_state.chat.append(("user", user_input))

    sql_query = generate_sql(schema, user_input)
    sql_query = clean_sql(sql_query)

    if not is_safe(sql_query):
        st.error("Unsafe query blocked 🚫")
        st.stop()

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

    except Exception as e:
        fixed_query = fix_sql(sql_query, str(e))
        fixed_query = clean_sql(fixed_query)

        try:
            with engine.connect() as conn:
                result = conn.execute(text(fixed_query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
            sql_query = fixed_query

        except Exception as e2:
            st.error(f"Query failed: {e2}")
            st.stop()

    st.session_state.chat.append(("sql", sql_query))
    st.session_state.chat.append(("result", df))


# Chat display
for role, content in st.session_state.chat:

    if role == "user":
        with st.chat_message("user"):
            st.write(content)

    elif role == "sql":
        with st.chat_message("assistant"):
            st.code(content, language="sql")

    elif role == "result":
        with st.chat_message("assistant"):
            st.dataframe(content)