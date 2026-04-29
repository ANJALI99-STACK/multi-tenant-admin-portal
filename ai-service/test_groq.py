import os
import time
import logging
from groq import Groq
from dotenv import load_dotenv
from services.groq_client import GroqClient

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqTestClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")

        self.client = Groq(api_key=api_key)

    def generate_response(self, prompt):
        try:
            start_time = time.time()

            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )

            duration = round(time.time() - start_time, 2)
            logger.info(f"Response received in {duration}s")

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            return None


if __name__ == "__main__":
    client = GroqClient()

    result = client.generate("Give 3 benefits of AI")

    if result:
        print("\nResponse:\n")
        print(result["content"])
        print("\nMetadata:", result)
    else:
        print("\nFailed after retries")