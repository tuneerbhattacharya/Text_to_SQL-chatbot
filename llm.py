import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(
    temperature=0,
    api_key=st.secrets["OPENAI_API_KEY"],
    model="gpt-4o-mini"
)

sql_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template="""
You are an expert MySQL assistant.

Schema:
{schema}

Question:
{question}

Rules:
- Only SELECT queries
- Use backticks for column names with spaces
- Do not hallucinate columns
- Add LIMIT 100
- Return ONLY raw SQL
- Do NOT include ``` or 'sql'

SQL:
"""
)

fix_prompt = PromptTemplate(
    input_variables=["query", "error"],
    template="""
Fix this SQL query based on error.

Query:
{query}

Error:
{error}

Return ONLY corrected SQL.
"""
)

def generate_sql(schema, question):
    prompt = sql_prompt.format(schema=schema, question=question)
    response = llm.invoke(prompt)
    return response.content.strip()

def fix_sql(query, error):
    prompt = fix_prompt.format(query=query, error=error)
    response = llm.invoke(prompt)
    return response.content.strip()