import re


def parse_sql_response(response: str):
    if not response:
        return None, ""

    sql_match = re.search(
        r"SQL:\s*(.*?)(?:Explanation:|$)",
        response,
        flags=re.IGNORECASE | re.DOTALL,
    )
    exp_match = re.search(
        r"Explanation:\s*(.*)",
        response,
        flags=re.IGNORECASE | re.DOTALL,
    )

    sql = sql_match.group(1).strip() if sql_match else response.strip()
    explanation = exp_match.group(1).strip() if exp_match else "No explanation returned."

    return sql, explanation
