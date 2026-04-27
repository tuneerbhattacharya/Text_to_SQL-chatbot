import streamlit as st


def hero(title: str, subtitle: str):
    st.title(title)
    st.caption(subtitle)


def metric_card(label: str, value):
    st.metric(label, value)


def show_sql_block(sql: str):
    st.subheader("Generated SQL")
    st.code(sql, language="sql")


def show_explanation_block(explanation: str):
    st.subheader("Explanation")
    st.info(explanation)


def sidebar_footer():
    st.caption("SaaS-ready • Auth • LCEL • RAG • Multi-DB • Export")