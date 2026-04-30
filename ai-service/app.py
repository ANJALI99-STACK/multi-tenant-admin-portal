from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from services.security import validate_input, verify_jwt

app = Flask(__name__)

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

# BEFORE REQUEST (JWT + validation)
@app.before_request
def before_request():
    # Skip auth for health endpoint
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
@app.route("/health", methods=["GET", "POST"])
def health():
    return {"status": "ok"}, 200


# Root endpoint
@app.route("/", methods=["GET"])
def home():
    return {"message": "AI Service Running"}, 200


# Security headers
@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    if "Server" in response.headers:
        del response.headers["Server"]

    return response


if __name__ == "__main__":
    app.run(port=5000, debug=False)