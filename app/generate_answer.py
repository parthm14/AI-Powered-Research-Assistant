# app/generate_answer.py

import google.generativeai as genai
from app.config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-pro")


def generate_response(query: str, context: str) -> str:
    """
    Uses Gemini Pro to generate an answer based on query and retrieved context.
    """
    prompt = (
        f"You are a helpful research assistant. Based on the following research context:\n\n"
        f"{context}\n\n"
        f"Answer the user's query:\n{query}"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {e}"