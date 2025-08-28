# resource_finder.py
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def find_resources(topic: str, max_results: int = 3) -> list:
    if not YOUTUBE_API_KEY:
        return [{"error": "YOUTUBE_API_KEY is not configured."}]

    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        search_query = f"{topic} tutorial explained"
        request = youtube.search().list(
            q=search_query, part='snippet', maxResults=max_results, type='video'
        )
        response = request.execute()

        videos = []
        # Return a list of dictionaries with title and URL
        for item in response.get('items', []):
            video_data = {
                "title": item['snippet']['title'],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video_data)

        return videos

    except HttpError as e:
        return [{"error": f"Could not fetch YouTube videos. Check API key/quota. Details: {e}"}]
