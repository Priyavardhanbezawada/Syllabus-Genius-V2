# content_generator.py
import os
from groq import Groq
import markdown

def generate_explanation(topic: str) -> str:
    """
    Uses the Groq API to generate a structured, exam-focused explanation of a topic.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "Error: GROQ_API_KEY is not configured."

        client = Groq(api_key=api_key)

        # This is a much more detailed prompt, modeled after your example.
        prompt = f"""
        You are an expert academic tutor. Your task is to provide a concise but deep explanation of the following topic, focusing on what a student needs to know for an exam.

        The topic is: "{topic}"

        Structure your response in Markdown format with the following sections:
        - **Definition:** A clear and concise definition of the topic.
        - **Key Concepts:** A bulleted list of 3-4 of the most critical sub-points or components, with a brief explanation for each.
        - **Importance:** A short paragraph explaining why this topic is important in its field and its real-world applications.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        # Convert the AI's Markdown response to HTML for proper display
        html_content = markdown.markdown(chat_completion.choices[0].message.content)
        return html_content

    except Exception as e:
        return f"Error: Failed to generate an explanation for this topic. Details: {e}"
