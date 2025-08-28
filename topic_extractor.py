# topic_extractor.py
import os
from groq import Groq

def extract_topics(text: str) -> list[str]:
    """
    This function uses the Groq API to intelligently extract key topics,
    concepts, or headings from any given text.
    """
    try:
        # Get the API key from the environment variables on Render
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return ["Error: GROQ_API_KEY is not configured in the environment."]

        client = Groq(api_key=api_key)
        
        # We only send the first 2500 characters to the AI to keep it fast and efficient.
        text_snippet = text[:2500]

        # This is the prompt that instructs the AI on what to do.
        prompt = f"""
        You are an expert at analyzing documents. Read the following text and identify the main topics, concepts, or headings.

        RULES:
        1. Return a simple list of strings, with each topic on a new line.
        2. Do NOT use numbers or bullet points (like * or -).
        3. Do NOT return any other text, explanation, or titles like "Extracted Topics:".
        4. Focus on phrases that represent key subjects in the document.

        Text to analyze:
        ---
        {text_snippet}
        ---
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192", # A fast and powerful model
        )
        
        response_content = chat_completion.choices[0].message.content
        
        # The AI returns a block of text with each topic on a new line.
        # We split this text into a Python list and remove any empty lines.
        topics = [line.strip() for line in response_content.split('\n') if line.strip()]
        
        if not topics:
            return ["No distinct topics were found in the document."]

        return topics

    except Exception as e:
        print(f"An error occurred while calling Groq API for topic extraction: {e}")
        return [f"Error: Failed to extract topics from Groq. Check the server logs."]
