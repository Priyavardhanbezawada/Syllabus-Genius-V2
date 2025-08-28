# content_generator.py
import os
from groq import Groq

def generate_explanation(topic: str) -> str:
    """
    Uses the Groq API to generate a concise, exam-focused explanation of a topic.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "Error: GROQ_API_KEY is not configured."

        client = Groq(api_key=api_key)

        # This prompt is specifically designed for exam preparation.
        prompt = f"""
        You are an expert academic tutor. Your task is to explain the following topic clearly and concisely, focusing on the key points that are most important for an exam.

        RULES:
        1. Start with a brief, one-sentence definition of the topic.
        2. List 3-4 of the most critical sub-points or concepts as bullet points.
        3. End with a short summary of why this topic is important.
        4. The entire explanation should be under 150 words.

        Topic: "{topic}"
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"An error occurred while calling Groq API for content generation: {e}")
        return "Error: Failed to generate an explanation for this topic."
