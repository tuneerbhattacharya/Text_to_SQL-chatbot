from sqlalchemy import create_engine, inspect, text
import pandas as pd


def create_db_engine(db_url: str):
    if not db_url:
        raise ValueError("Database URL is empty.")

    if db_url.startswith("mysql://"):
        db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)

    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)

    return create_engine(db_url, pool_pre_ping=True)


def get_schema_chunks(engine):
    inspector = inspect(engine)
    chunks = []

    for table in inspector.get_table_names():
        columns = inspector.get_columns(table)
        column_lines = [f"{col['name']} ({col['type']})" for col in columns]

        chunk = f"Table: {table}\nColumns:\n- " + "\n- ".join(column_lines)

        pk = inspector.get_pk_constraint(table).get("constrained_columns", [])
        if pk:
            chunk += f"\nPrimary Key: {', '.join(pk)}"

        fk = inspector.get_foreign_keys(table)
        if fk:
            fk_lines = []
            for item in fk:
                fk_lines.append(
                    f"{item.get('constrained_columns')} references "
                    f"{item.get('referred_table')}({item.get('referred_columns')})"
                )
            chunk += "\nForeign Keys:\n- " + "\n- ".join(fk_lines)

        chunks.append(chunk)

    return chunks


def run_query(engine, query: str):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall(), result.keys()


def save_csv_to_sqlite(df: pd.DataFrame, engine, table_name: str):
    safe_table_name = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in table_name)
    df.to_sql(safe_table_name, engine, if_exists="replace", index=False)
    return safe_table_name
