# flashcard_generator.py
import os
import json
import re
from groq import Groq

def generate_flashcards(topic: str, num_cards: int = 5):
    """
    Generates a set of flashcards (question/answer pairs) for a given topic using the Groq API.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"error": "GROQ_API_KEY is not configured."}

        client = Groq(api_key=api_key)

        prompt = f"""
        You are an expert at creating study materials. Generate {num_cards} flashcards for the topic: "{topic}".

        RULES:
        1. Your response must be ONLY a valid JSON object.
        2. The JSON object must have a single key "flashcards", which is an array of card objects.
        3. Each card object must have two keys: "front" (the question or term) and "back" (the answer or definition).
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        response_content = chat_completion.choices[0].message.content

        # --- FIX: Safely extract the JSON from the response ---
        # This regular expression finds the JSON block, even if the AI adds extra text.
        json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        else:
            return {"error": "Could not find a valid JSON object in the AI's response."}

    except Exception as e:
        # The original error "Expecting value..." will be caught here.
        return {"error": f"Failed to generate flashcards from Groq: {e}"}
