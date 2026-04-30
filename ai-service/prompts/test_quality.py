import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.groq_client import GroqClient

client = GroqClient()
# 10 fresh inputs
inputs = [
    "SQL injection in login form",
    "Phishing email targeting employees",
    "Weak password policy in company",
    "Customer data breach scenario",
    "Malware infection via attachment",
    "Insider leaking confidential data",
    "Unpatched system vulnerability",
    "Ransomware attack on hospital",
    "Cloud storage misconfiguration",
    "Social engineering phone scam"
]


def run_test(prompt_template):
    scores = []

    for i, inp in enumerate(inputs, 1):
        print(f"\n--- Test {i} ---")
        print("Input:", inp)

        prompt = prompt_template.format(input_text=inp)

        response = client.generate(prompt)
        output = response["content"] if response else "No response"

        print("Output:\n", output)

        score = int(input("Score (1-5): "))
        scores.append(score)

    avg = sum(scores) / len(scores)
    print("\nAverage Score:", round(avg, 2))


# SIMPLE PROMPT (keep it strict)
PROMPT = """
You are a cybersecurity assistant.

Respond STRICTLY in this format. Do NOT add extra text.

Definition: (max 2 sentences)
Impact: (max 2 sentences)
Example: (1 short real-world example)

Rules:
- No bullet points
- No headings like ** or titles
- No extra explanation
- Keep answer concise and structured

Input: {input_text}
"""

run_test(PROMPT)