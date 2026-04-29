from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# =========================
# DAY 2: PRIMARY PROMPT
# =========================
PRIMARY_PROMPT = """
You are CampusPe AI, a student-friendly text analysis assistant.

Your job is to analyze user input and respond in a structured, simple, and helpful way.

Rules:
- Understand the input carefully
- Provide clear explanation or analysis
- Keep responses short and structured
- If input is unclear, ask a clarification question
- Do not hallucinate or assume facts

Output format:
- Summary
- Key insights
- Sentiment (if applicable)

User Input:
{text}

Response:
"""


@app.route("/")
def home():
    return {"message": "AI Service Running"}


@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "healthy",
        "message": "AI Service is running"
    }


@app.route("/describe", methods=["POST"])
def describe():
    start_time = time.time()

    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({
                "status": "error",
                "message": "Please provide 'text' in request body"
            }), 400

        text = data["text"]

        # =========================
        # BASIC ANALYSIS (DAY 1 LOGIC)
        # =========================
        words = text.split()
        word_count = len(words)
        char_count = len(text)

        summary = " ".join(words[:5]) if words else ""

        positive_words = ["good", "great", "happy", "excellent", "awesome", "nice", "love"]
        negative_words = ["bad", "sad", "terrible", "worst", "poor", "hate"]

        sentiment = "neutral"
        for word in words:
            lw = word.lower()
            if lw in positive_words:
                sentiment = "positive"
                break
            elif lw in negative_words:
                sentiment = "negative"
                break

        # =========================
        # DAY 2 PROMPT INTEGRATION
        # =========================
        prompt_used = PRIMARY_PROMPT.format(text=text)

        response_time = round((time.time() - start_time) * 1000, 2)

        return jsonify({
            "status": "success",
            "input_text": text,

            # Prompt layer (Day 2 addition)
            "prompt_used": prompt_used,

            # Analysis output
            "analysis": {
                "word_count": word_count,
                "character_count": char_count,
                "summary": summary,
                "sentiment": sentiment
            },

            "meta": {
                "response_time_ms": response_time
            },

            "message": "Text analyzed successfully using CampusPe Day 2 prompt system"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Something went wrong",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)