import streamlit as st
from sqlalchemy import create_engine, text

def get_engine():
    db_url = st.secrets["MYSQL_URL"].replace("mysql://", "mysql+pymysql://")
    return create_engine(db_url)

def get_schema(engine):
    schema = ""
    with engine.connect() as conn:
        tables = conn.execute(text("SHOW TABLES")).fetchall()

        for table in tables:
            table_name = table[0]
            schema += f"\nTable: {table_name}\n"

            columns = conn.execute(
                text(f"SHOW COLUMNS FROM `{table_name}`")
            ).fetchall()

            for col in columns:
                schema += f"- {col[0]} ({col[1]})\n"

    return schema