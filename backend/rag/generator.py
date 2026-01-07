from groq import Groq
from backend.config import settings


class Generator:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate_answer(self, query: str, contexts: list[dict]) -> str:
        context_text = "\n\n".join(
            f"- {c['text']}" for c in contexts
        )

        prompt = f"""
You are a medical assistant.
Answer the user's question ONLY using the context provided below.
If the answer is not present in the context, say:
"I don't have enough information from the provided documents."

Context:
{context_text}

Question:
{query}

Answer clearly and concisely. Do not add external knowledge.
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()
