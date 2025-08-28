# flashcard_generator.py
import os
import json
import re
from groq import Groq

def generate_flashcards(topic: str, num_cards: int = 5):
    """
    Generates a set of flashcards for a given topic using the Groq API.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"error": "GROQ_API_KEY is not configured."}

        client = Groq(api_key=api_key)

        # Updated prompt
        prompt = f"""
        You are an expert at creating study materials. Generate {num_cards} flashcards for the topic: "{topic}".

        RULES:
        1. Your response must contain ONLY a valid JSON object enclosed in a ```json ... ``` markdown block.
        2. Do not include any text before or after the markdown block.
        3. The JSON object must have a key "flashcards", which is an array of card objects.
        4. Each card object must have two keys: "front" and "back".
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
            return json.loads(response_content)

    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse flashcards from Groq. The AI returned invalid JSON. Error: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
