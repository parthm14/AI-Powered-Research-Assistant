import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

# Async summarization function
async def summarize_text(text):
    if not text.strip():
        return "No content to summarize."
    try:
        prompt = f"Please summarize the following academic abstract bullet points. Avoid repetition, use clear language, and extract key ideas only:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during summarization: {str(e)}"