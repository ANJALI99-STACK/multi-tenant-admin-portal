from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import time

from services.security import validate_input, verify_jwt
from services.groq_client import GroqClient

app = Flask(__name__)

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

# Groq client
groq = GroqClient()


# BEFORE REQUEST (JWT + validation)
@app.before_request
def before_request():
    # Skip auth for health
    if request.path == "/health":
        return None

    # JWT check
    auth_error = verify_jwt()
    if auth_error:
        return auth_error

    # Input validation for POST
    if request.method == "POST":
        return validate_input()


# Health endpoint
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200


# Root endpoint
@app.route("/", methods=["GET"])
def home():
    return {"message": "AI Service Running"}, 200


# -------------------------------
# DESCRIBE ENDPOINT
# -------------------------------
@app.route("/describe", methods=["POST"])
def describe():
    start_time = time.time()

    data = request.get_json()
    user_input = data["input"]

    prompt = f"""
Provide:
- Definition
- Impact
- Example

Input: {user_input}
"""

    response = groq.generate(prompt)

    if not response:
        return jsonify({"error": "AI service failed"}), 500

    return jsonify({
        "status": "success",
        "input": user_input,
        "output": response["content"],
        "generated_at": datetime.utcnow().isoformat(),
        "meta": {
            "response_time": response["response_time"]
        }
    })


# -------------------------------
# RECOMMEND ENDPOINT
# -------------------------------
@app.route("/recommend", methods=["POST"])
def recommend():
    start_time = time.time()

    data = request.get_json()
    user_input = data["input"]

    prompt = f"""
Give exactly 3 short actionable recommendations.

Input: {user_input}
"""

    response = groq.generate(prompt)

    if not response:
        return jsonify({"error": "AI service failed"}), 500

    raw_output = response["content"]

    lines = raw_output.split("\n")
    clean_lines = [
        l.strip("-•123456789. ").strip()
        for l in lines if l.strip()
    ][:3]

    while len(clean_lines) < 3:
        clean_lines.append("Improve security practices")

    recommendations = []
    for i, line in enumerate(clean_lines):
        recommendations.append({
            "action_type": f"Action {i+1}",
            "description": line,
            "priority": "high" if i == 0 else "medium"
        })

    return jsonify({
        "status": "success",
        "input": user_input,
        "recommendations": recommendations,
        "generated_at": datetime.utcnow().isoformat(),
        "meta": {
            "response_time": response["response_time"]
        }
    })


# -------------------------------
# SECURITY HEADERS
# -------------------------------
@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    if "Server" in response.headers:
        del response.headers["Server"]

    return response


# Run app
if __name__ == "__main__":
    app.run(port=5000, debug=False)