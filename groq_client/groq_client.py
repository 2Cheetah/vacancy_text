import os
import logging
from groq import Groq


class GroqClient:
    def __init__(self, api_token: str) -> Groq:
        self.client = Groq(api_key=api_token)

    def get_bot_answer(self, prompt: str) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="deepseek-r1-distill-llama-70b",
            )
            answer = chat_completion.choices[0].message.content
            return answer
        except Exception as e:
            logging.error(f"An error occured while trying to get chat completion. Error: {e}")
            return ""


if __name__ == "__main__":
    api_token = os.getenv("GROQ_API_TOKEN")
    groq_client = GroqClient(api_token)
    print(groq_client.get_bot_answer("Hello, World!"))
