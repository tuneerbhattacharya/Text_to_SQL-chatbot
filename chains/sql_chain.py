from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def build_sql_chain(openai_key: str, model_name: str = "gpt-4o-mini"):
    llm = ChatOpenAI(
        api_key=openai_key,
        model=model_name,
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_template("""
You are a senior data analyst and SQL expert.

Relevant schema context from RAG:
{context}

Full detected schema:
{schema}

Conversation history:
{history}

User role:
{role}

User question:
{question}

Rules:
- Generate ONLY read-only SQL.
- Only SELECT or WITH queries are allowed.
- Never generate DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, CREATE, GRANT, REVOKE, CALL, EXEC.
- Use only tables and columns that exist in the schema.
- Use correct joins when relationships are obvious.
- Use backticks for MySQL identifiers with spaces.
- Add LIMIT 100 unless aggregate-only.
- Resolve follow-up questions using conversation history.

Return exactly this format:

SQL:
<valid SQL query>

Explanation:
<brief explanation>
""")

    return prompt | llm | StrOutputParser()
