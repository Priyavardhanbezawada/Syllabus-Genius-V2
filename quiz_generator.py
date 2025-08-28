# quiz_generator.py
import os
import json
from groq import Groq

def generate_quiz(topic: str, num_questions: int = 5):
    """
    Generates a varied quiz for a given topic using the Groq API.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"error": "GROQ_API_KEY is not configured."}

        client = Groq(api_key=api_key)

        prompt = f"""
        You are an expert at creating engaging and effective study quizzes for university students.
        Generate a {num_questions}-question quiz on the topic: "{topic}".

        RULES:
        1. Create a mix of question types: multiple-choice, true/false, and fill-in-the-blank.
        2. Your response must be ONLY a valid JSON object. Do not include any text, explanation, or markdown.
        3. The JSON object must have a single key "quiz", which is an array of question objects.
        4. Each question object must have:
           - "type": "multiple-choice", "true-false", or "fill-in-the-blank".
           - "question": The question text. For fill-in-the-blank, use "____" for the blank space.
           - "options": An array of strings for multiple-choice, or ["True", "False"] for true/false. Leave this empty for fill-in-the-blank.
           - "answer": The correct answer string.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)

    except Exception as e:
        return {"error": f"Failed to generate quiz from Groq: {e}"}
