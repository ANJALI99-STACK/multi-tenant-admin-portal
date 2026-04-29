import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.groq_client import GroqClient

client = GroqClient()

# Load prompt
with open("prompts/describe.txt", "r") as f:
    system_prompt = f.read()

# Load inputs
with open("prompts/test_inputs.txt", "r") as f:
    inputs = [line.strip() for line in f if line.strip()]

scores = []

for i, user_input in enumerate(inputs, start=1):
    print(f"\n--- Test {i} ---")
    print("Input:", user_input)

    result = client.generate(
        user_input,
        system_prompt=system_prompt
    )

    if result:
        output = result["content"]
        print("Output:\n", output)

        score = int(input("Score (1-10): "))
        scores.append(score)
    else:
        print("Failed")
        scores.append(0)

avg = sum(scores) / len(scores)
print(f"\nAverage Score: {round(avg, 2)}")