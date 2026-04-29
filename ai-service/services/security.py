import re
from flask import request, jsonify


def strip_html(text: str) -> str:
    """Remove HTML tags from input"""
    return re.sub(r"<.*?>", "", text)


def detect_prompt_injection(text: str) -> bool:
    """Basic detection of prompt injection patterns"""
    suspicious_patterns = [
        "ignore previous instructions",
        "system prompt",
        "act as",
        "jailbreak",
        "override",
        "bypass"
    ]

    text_lower = text.lower()
    return any(pattern in text_lower for pattern in suspicious_patterns)



def validate_input():
    data = request.get_json()

    # 1. Empty input check
    if not data or "input" not in data or not data["input"].strip():
        return jsonify({"error": "Invalid input"}), 400

    user_input = data["input"].lower()

    # 2. Prompt injection detection
    if "ignore previous instructions" in user_input or "act as admin" in user_input:
        return jsonify({"error": "Prompt injection detected"}), 400

    # 3. SQL injection detection (NEW FIX)
    sql_patterns = [
        r"select\s.*from",
        r"drop\s+table",
        r"insert\s+into",
        r"delete\s+from",
        r"--",
        r";"
    ]

    for pattern in sql_patterns:
        if re.search(pattern, user_input):
            return jsonify({"error": "SQL injection detected"}), 400

    return None