# concept_mapper.py
import os
from groq import Groq
import markdown

def generate_concept_map(topics: list[str]) -> str:
    """
    Uses the Groq API to analyze a list of topics and explain the relationships between them.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "Error: GROQ_API_KEY is not configured."

        client = Groq(api_key=api_key)

        # Convert the list of topics into a single string for the prompt
        topic_list_str = "\n- ".join(topics)

        prompt = f"""
        You are a university professor and an expert in curriculum design.
        Analyze the following list of topics from a course syllabus and generate a "big picture" overview.

        Your task is to explain the narrative of the course. Describe how the topics connect and build upon one another. Identify foundational concepts and explain why they are important for later, more advanced topics.

        RULES:
        1. Structure your response in clear, easy-to-read Markdown.
        2. Start with a brief summary of the course's overall journey.
        3. Use bold text to highlight key topic names when you mention them.
        4. Keep the entire analysis concise, under 250 words.

        Course Topics:
        - {topic_list_str}
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        # Convert the AI's Markdown response into HTML for proper display
        html_content = markdown.markdown(chat_completion.choices[0].message.content)
        return html_content

    except Exception as e:
        return f"Error: Failed to generate the concept map. Details: {e}"
