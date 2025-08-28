# quiz_generator.py
import os
import json
import re
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

        # Updated prompt: Asks the AI to wrap the JSON in a markdown block.
        prompt = f"""
        You are an expert at creating study quizzes. Generate a {num_questions}-question quiz on the topic: "{topic}".

        RULES:
        1. Create a mix of question types: multiple-choice, true/false, and fill-in-the-blank.
        2. Your response must contain ONLY a valid JSON object enclosed in a ```json ... ``` markdown block.
        3. Do not include any text or explanation before or after the markdown block.
        4. The JSON object must have a key "quiz" which is an array of question objects.
        5. Each question object must have "type", "question", "options" (empty for fill-in-the-blank), and "answer".
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        response_content = chat_completion.choices[0].message.content

        # --- FIX: Reliably extract the JSON from the response ---
        json_match = re.search(r'```json\n({.*?})\n```', response_content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            return json.loads(json_str)
        else:
            # Fallback for cases where the AI doesn't follow instructions perfectly
            return json.loads(response_content)

    except json.JSONDecodeError as e:
        # This will catch the exact errors you were seeing
        return {"error": f"Failed to parse quiz from Groq. The AI returned invalid JSON. Error: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
