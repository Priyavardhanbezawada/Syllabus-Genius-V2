# quiz_generator.py
import os
import json
import re
from groq import Groq

def generate_quiz(topic: str, num_questions: int = 5):
    """
    Generates a varied quiz for a given topic using the Groq API,
    with robust error handling for empty or invalid JSON responses.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"error": "GROQ_API_KEY is not configured."}

        client = Groq(api_key=api_key)

        prompt = f"""
        You are an expert quiz creator. Generate a {num_questions}-question quiz on the topic: "{topic}".

        RULES:
        1. Your response must contain ONLY a valid JSON object.
        2. Do not include any text, explanation, or markdown formatting like ```json.
        3. The JSON must have a key "quiz" which is an array of question objects.
        4. Each object must have "type", "question", "options", and "answer" keys.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        response_content = chat_completion.choices[0].message.content.strip()

        # --- FIX: Check for an empty response before trying to parse ---
        if not response_content:
            print("Groq API returned an empty response for the quiz.")
            return {"error": "The AI failed to generate a quiz for this topic. Please try again."}

        # Attempt to parse the JSON
        return json.loads(response_content)

    except json.JSONDecodeError:
        # This will catch the exact error you were seeing if the response is not empty but still invalid.
        print(f"Invalid JSON received from Groq: {response_content}")
        return {"error": "The AI returned an invalid format for the quiz. Please try again."}
    except Exception as e:
        print(f"An unexpected error occurred in quiz generation: {e}")
        return {"error": f"An unexpected error occurred: {e}"}
