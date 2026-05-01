# AI SERVICE — SUMMARY CARD

---

## 🔹 Overview

AI-powered service that securely processes user input and generates structured responses using a language model.
Designed with strong validation, security controls, and consistent output formatting.

---

## 🔹 Key Endpoints

### 1. `/describe`

* Generates structured AI explanation
* Output includes:

  * Definition
  * Impact
  * Example

---

### 2. `/recommend`

* Generates 3 actionable recommendations
* Output:

  * Prioritized suggestions
  * Clean structured format

---

### 3. `/health`

* Service health check
* Output:

  * `{"status": "ok"}`

---

## 🔹 Tech Stack

* **Backend:** Flask (Python)
* **AI Model:** Groq (LLaMA 3)
* **Authentication:** JWT (PyJWT)
* **Rate Limiting:** Flask-Limiter
* **Testing:** Pytest
* **Security Testing:** OWASP ZAP
* **Containerization:** Docker

---

## 🔹 Security Features

* JWT-based authentication (protected endpoints)
* Input validation (rejects empty/malformed input)
* SQL injection detection & blocking
* Prompt injection detection
* Rate limiting (30 requests/minute per IP)
* Secure HTTP headers (CSP, XSS, nosniff, frame protection)
* API key protection using `.env`

---

## 🔹 System Flow

User Input → Validation → Security Checks → AI Processing → Structured Response

---

## 🔹 GitHub Repository

 https://github.com/tecsxpert/multi-tenant-admin-portal

---

## 🔹 Status

✔ Secure
✔ Tested
✔ Containerized
✔ Ready for Integration

---
