# app/generate_answer.py

import google.generativeai as genai
from app.config import GOOGLE_API_KEY

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-pro")

def generate_response(question: str, context: str, history: list = None) -> str:
    """
    Returns a complete Gemini AI answer (non-streaming).
    """
    if history is None:
        history = []

    history_text = "\n".join(
        [f"User: {msg['user']}\nAI: {msg['ai']}" for msg in history]
    )

    prompt = f"""
You are an AI assistant helping the user understand research papers.
Context from retrieved papers:
{context}

Conversation so far:
{history_text}

User: {question}
AI:
"""

    response = model.generate_content(prompt)
    answer = response.text.strip() if hasattr(response, "text") else ""

    # Save to history
    history.append({"user": question, "ai": answer})
    return answer