# quiz_generator.py
import os
import json
import re
from groq import Groq

def generate_quiz(topic: str, num_questions: int = 5):
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"error": "GROQ_API_KEY is not configured."}

        client = Groq(api_key=api_key)
        prompt = f"""
        Generate a {num_questions}-question quiz on the topic: "{topic}".
        RULES: Your response must contain ONLY a valid JSON object. Do not include any other text or markdown.
        The JSON must have a "quiz" key, which is an array of objects, each with "type", "question", "options", and "answer".
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        response_content = chat_completion.choices[0].message.content.strip()

        # --- FIX: Reliably find the JSON block in the response ---
        json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
        if not json_match:
            return {"error": "The AI response did not contain a valid quiz format."}

        return json.loads(json_match.group(0))

    except json.JSONDecodeError:
        return {"error": "The AI returned an invalid format for the quiz. Please try again."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
