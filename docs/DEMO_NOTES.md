# DAY 18 — DEMO (AI + Flask + Groq)

## 1. Show health endpoint
curl.exe http://127.0.0.1:5000/health

This confirms the service is running and accessible.


## 2. Show AI Recommend
curl.exe -X POST "http://127.0.0.1:5000/recommend" -H "Authorization: Bearer <TOKEN>" -d '{"input":"phishing attack"}'

Here, the AI generates actionable recommendations based on the input.

## 3. Show AI Describe (Generate Report)
curl.exe -X POST "http://127.0.0.1:5000/describe" -H "Authorization: Bearer <TOKEN>" -d '{"input":"SQL injection attack"}'

This generates a structured report — including definition, impact, and example.


# 60-sec explanation (Flask + Groq)

We built this service using Flask, which handles API routing and request processing.

When a request comes in, it first goes through validation and security checks.

If the input is valid, we send it to Groq, which runs the AI model and generates a response.

We then format that response into a structured output and return it to the user.

So Flask manages the application flow, and Groq handles the AI processing.