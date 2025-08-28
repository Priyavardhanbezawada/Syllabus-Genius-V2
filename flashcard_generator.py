# flashcard_generator.py
import os
import json
import re
from groq import Groq

def generate_flashcards(topic: str, num_cards: int = 5):
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"error": "GROQ_API_KEY is not configured."}

        client = Groq(api_key=api_key)
        prompt = f"""
        Generate {num_cards} flashcards for the topic: "{topic}".
        RULES: Your response must contain ONLY a valid JSON object.
        The JSON must have a "flashcards" key, which is an array of objects, each with "front" and "back".
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        response_content = chat_completion.choices[0].message.content.strip()

        # --- FIX: Reliably find the JSON block in the response ---
        json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
        if not json_match:
            return {"error": "The AI response did not contain a valid flashcard format."}

        return json.loads(json_match.group(0))

    except json.JSONDecodeError:
        return {"error": "The AI returned an invalid format for the flashcards. Please try again."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
