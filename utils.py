def is_safe(query):
    unsafe = ["drop", "delete", "truncate", "update", "insert", "alter"]
    return not any(word in query.lower() for word in unsafe)


def clean_sql(query):
    query = query.replace("```sql", "").replace("```", "")
    query = query.replace("sql\n", "").strip()
    return query