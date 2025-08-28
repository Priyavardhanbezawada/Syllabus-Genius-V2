# resource_finder.py
import os
from groq import Groq
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys

# Load both API keys from the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_keywords(topic: str) -> str:
    """
    Uses the Groq API to analyze a topic and extract the best keywords for a YouTube search.
    """
    try:
        if not GROQ_API_KEY:
            # If Groq isn't available, just use the original topic
            return topic

        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = f"""
        Analyze the following academic topic and extract the 3-5 most important keywords that would be best for finding a high-quality tutorial video on YouTube.

        RULES:
        1. Return ONLY the keywords, separated by a space.
        2. Do not add any other text, explanation, or punctuation.

        Topic: "{topic}"

        Keywords:
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        
        keywords = chat_completion.choices[0].message.content.strip()
        
        # A simple check to ensure the AI returned something reasonable
        if keywords and len(keywords) < len(topic) * 1.5:
            return keywords
        else:
            # Fallback to the original topic if the AI response is strange
            return topic

    except Exception as e:
        print(f"An error occurred while getting keywords from Groq: {e}", file=sys.stderr)
        # If there's an error, we can still proceed with the original topic
        return topic

def find_resources(topic: str, max_results: int = 3) -> list:
    """
    Finds the top YouTube video tutorials for a given topic using AI-generated keywords.
    """
    if not YOUTUBE_API_KEY:
        return [{"error": "YOUTUBE_API_KEY is not configured."}]

    try:
        # --- NEW: Get AI-powered keywords first ---
        search_keywords = get_youtube_keywords(topic)
        
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # Use the keywords for a more precise search
        request = youtube.search().list(
            q=f"{search_keywords} tutorial",
            part='snippet',
            maxResults=max_results,
            type='video'
        )
        response = request.execute()
        
        videos = []
        for item in response.get('items', []):
            video_data = {
                "title": item['snippet']['title'],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video_data)
        
        return videos
            
    except HttpError as e:
        return [{"error": f"Could not fetch YouTube videos. Check API key/quota. Details: {e}"}]
