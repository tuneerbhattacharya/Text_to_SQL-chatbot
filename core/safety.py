import re

FORBIDDEN_KEYWORDS = [
    "DROP", "DELETE", "UPDATE", "ALTER", "INSERT", "TRUNCATE",
    "CREATE", "REPLACE", "GRANT", "REVOKE", "MERGE", "CALL", "EXEC"
]


def clean_sql(query: str) -> str:
    if not query:
        return ""

    query = query.strip()
    query = query.replace("```sql", "").replace("```", "").strip()

    if query.lower().startswith("sql\n"):
        query = query[4:].strip()

    match = re.search(r"\b(SELECT|WITH)\b", query, flags=re.IGNORECASE)
    if match:
        query = query[match.start():].strip()

    return query


def is_safe_sql(query: str) -> bool:
    if not query:
        return False

    q = query.upper()

    if not (q.lstrip().startswith("SELECT") or q.lstrip().startswith("WITH")):
        return False

    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", q):
            return False

    stripped = query.strip()
    if ";" in stripped[:-1]:
        return False

    return True
