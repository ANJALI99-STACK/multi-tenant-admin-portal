import os
import time
import logging
from typing import Optional, Dict, Any

from groq import Groq
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("groq_client")


class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in environment variables")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,   # 🔥 lower for consistency
        max_tokens: int = 150,
        retries: int = 3
    ) -> Optional[Dict[str, Any]]:

        for attempt in range(1, retries + 1):
            try:
                start_time = time.time()

                messages = []

                if system_prompt:
                    messages.append({
                    "role": "system",
                    "content": system_prompt
                    })
                else:
                    messages.append({
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    })

                messages.append({
                    "role": "user",
                    "content": prompt
                })

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                duration = round(time.time() - start_time, 2)
                content = response.choices[0].message.content

                return {
                    "content": content,
                    "model": self.model,
                    "response_time": duration,
                    "attempt": attempt
                }

            except Exception as e:
                time.sleep(2 ** attempt)

        return None