# LESSONS LEARNED — AI SERVICE

---

## 🔹 Overview

This document summarizes key learnings, challenges, and improvements identified during the development and testing of the AI service.

---

## 🔹 Key Learnings

* **Input validation is critical**
  All user input must be validated before reaching the AI model to prevent misuse and ensure system stability.

* **Prompt design impacts output quality**
  Well-structured prompts significantly improve consistency, clarity, and reliability of AI responses.

* **Security should be built early**
  Implementing authentication, validation, and protection mechanisms from the beginning avoids major issues later.

* **Testing improves confidence**
  Unit testing and security testing (Pytest, OWASP ZAP) helped verify correctness and robustness.

* **Separation of concerns is important**
  Keeping AI logic, validation, and routing separate makes the system easier to maintain and scale.

---

## 🔹 Challenges Faced

* **Handling prompt injection attempts**
  Designing rules to detect and block malicious instructions required careful consideration.

* **Ensuring consistent AI output format**
  Early responses were inconsistent until strict prompt structure was enforced.

* **Balancing strict validation vs usability**
  Needed to block malicious inputs without affecting valid user requests.

* **Environment limitations (Docker permissions)**
  Docker execution was restricted, so equivalent validation was performed using application restart.

---

## 🔹 Improvements for Future Sprints (features)

* Implement **role-based access control (RBAC)**
* Use **secure secret management systems** instead of static keys
* Deploy with **Gunicorn + Nginx** for production readiness
* Add **logging and monitoring** for better observability
* Enhance **prompt injection detection** using advanced techniques
* Introduce **automated integration testing**

---

## 🔹 Feedback & Reflection

This project provided practical experience in building a secure AI-powered service.
It highlighted the importance of combining backend engineering, AI integration, and security practices.

Working through real-world challenges improved problem-solving skills and understanding of production-level system design.

---

## 🔹 Conclusion

The AI service evolved from a basic implementation to a secure, tested, and structured system.
The lessons learned will guide future development and improvements in scalability, security, and reliability.

---
