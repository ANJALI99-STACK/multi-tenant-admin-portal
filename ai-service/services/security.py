import re
from flask import request, jsonify
import jwt


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

    # 2. Sanitize input
    user_input = strip_html(data["input"]).lower()

    # 3. Prompt injection detection (FIXED)
    if detect_prompt_injection(user_input):
        return jsonify({"error": "Prompt injection detected"}), 400

    # 4. SQL injection detection
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


# JWT
SECRET_KEY = "secret123"  # simple for assignment


def verify_jwt():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401

    token = auth_header.split(" ")[1]

    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    return None