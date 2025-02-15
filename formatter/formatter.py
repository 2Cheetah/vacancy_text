import os

from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_TOKEN"),
)


def format_text(groq_client, text, format):
    prompt = f"""Отформатируй текст ниже в соответствии с форматом указанным после текста. Только отформатированный текст, никакой дополнительной информации, никаких вопросов. Только на русском языке.
Необходимо из текста выделить блоки информации: "О компании", "Обязанности", "Требования", "Условия" и отформатировать в соответствии с форматом указанным ниже. Информация в блоках не должна повторяться.
Текст:
{text}

Формат:
{format}
"""
    formatted_text = get_bot_answer(groq_client, prompt)
    return formatted_text


def get_bot_answer(groq_client: Groq, prompt: str) -> str:
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        answer = chat_completion.choices[0].message.content
        return answer
    except:
        return ""
