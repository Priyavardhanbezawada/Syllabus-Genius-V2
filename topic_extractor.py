# topic_extractor.py
import os
import re
from groq import Groq

def extract_topics(text: str) -> list[str]:
    """
    Extracts key topics from any text using the Groq API.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return ["Error: GROQ_API_KEY is not configured."]

        client = Groq(api_key=api_key)
        
        # We provide a snippet of the text to keep the prompt efficient
        text_snippet = text[:2000]

        prompt = f"""
        You are an expert at analyzing academic documents.
        Read the following text and identify the main topics or chapter headings.
        RULES:
        1. Return a simple list of strings.
        2. Do not number the list or use bullet points.
        3. Each topic should be on a new line.
        4. Do not return any other text, explanation, or titles.

        Text to analyze:
        ---
        {text_snippet}
        ---
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        
        response_content = chat_completion.choices[0].message.content
        
        # Split the response by newlines to get a list of topics
        topics = [line.strip() for line in response_content.split('\n') if line.strip()]
        
        return topics if topics else ["No distinct topics were found."]

    except Exception as e:
        print(f"An error occurred while calling Groq API for topic extraction: {e}")
        return [f"Error: Failed to extract topics from Groq. Details: {e}"]
