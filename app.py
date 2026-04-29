from flask import Flask, request, jsonify
import time
from datetime import datetime
import os
from groq import Groq
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PRIMARY_PROMPT = """
You are a helpful assistant.

Provide:
- Summary
- Key insights
- Sentiment

User Input:
{text}
"""

RECOMMEND_PROMPT = """
Give 3 short actionable recommendations for this input.

User Input:
{text}
"""


@app.route("/")
def home():
    return {"message": "AI Service Running"}


@app.route("/health")
def health():
    return {"status": "healthy"}


@app.route("/describe", methods=["POST"])
def describe():
    start_time = time.time()

    try:
        data = request.get_json()

        if not data or "input" not in data:
            return jsonify({"error": "Missing 'input'"}), 400

        user_input = data["input"]
        prompt = PRIMARY_PROMPT.format(text=user_input)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content

        return jsonify({
            "status": "success",
            "input": user_input,
            "output": output,
            "generated_at": datetime.utcnow().isoformat(),
            "meta": {
                "response_time_ms": round((time.time() - start_time) * 1000, 2)
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/recommend", methods=["POST"])
def recommend():
    start_time = time.time()

    try:
        data = request.get_json()

        if not data or "input" not in data:
            return jsonify({"error": "Missing 'input'"}), 400

        user_input = data["input"]
        prompt = RECOMMEND_PROMPT.format(text=user_input)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response.choices[0].message.content

        lines = raw_output.split("\n")
        clean_lines = [
            l.strip("-•123456789. ").strip()
            for l in lines
            if l.strip() and not l.lower().startswith("here are")
        ]

        clean_lines = clean_lines[:3]

        while len(clean_lines) < 3:
            clean_lines.append("Improve skills through consistent practice")

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
                "response_time_ms": round((time.time() - start_time) * 1000, 2)
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to generate recommendations",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)