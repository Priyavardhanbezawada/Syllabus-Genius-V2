# flashcard_generator.py
import os
import json
import re
from groq import Groq

def generate_flashcards(topic: str, num_cards: int = 5):
    """
    Generates a set of flashcards for a given topic using the Groq API,
    with robust error handling for empty or invalid JSON responses.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"error": "GROQ_API_KEY is not configured."}

        client = Groq(api_key=api_key)

        prompt = f"""
        You are an expert at creating study materials. Generate {num_cards} flashcards for the topic: "{topic}".

        RULES:
        1. Your response must contain ONLY a valid JSON object.
        2. Do not include any text, explanation, or markdown formatting like ```json.
        3. The JSON must have a key "flashcards", which is an array of card objects.
        4. Each card object must have two keys: "front" and "back".
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        response_content = chat_completion.choices[0].message.content.strip()

        # --- FIX: Check for an empty response before trying to parse ---
        if not response_content:
            print("Groq API returned an empty response for flashcards.")
            return {"error": "The AI failed to generate flashcards for this topic. Please try again."}

        # Attempt to parse the JSON
        return json.loads(response_content)

    except json.JSONDecodeError:
        # This will catch the error if the response is not empty but still invalid.
        print(f"Invalid JSON received from Groq: {response_content}")
        return {"error": "The AI returned an invalid format for the flashcards. Please try again."}
    except Exception as e:
        print(f"An unexpected error occurred in flashcard generation: {e}")
        return {"error": f"An unexpected error occurred: {e}"}
