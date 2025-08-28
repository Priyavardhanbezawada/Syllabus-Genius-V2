# flashcard_generator.py
import os
import json
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
        4. The questions should be concise and perfect for a flashcard format.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)

    except Exception as e:
        return {"error": f"Failed to generate flashcards from Groq: {e}"}
