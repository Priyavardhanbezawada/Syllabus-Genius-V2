# resource_finder.py
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys

# Load the secret API keys from the environment
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def find_youtube_videos(topic: str, max_results: int = 3) -> list:
    """Finds top YouTube video tutorials for a given topic."""
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        search_query = f"{topic} tutorial explained"

        request = youtube.search().list(
            q=search_query,
            part='snippet',
            maxResults=max_results,
            type='video'
        )
        response = request.execute()

        videos = []
        for item in response.get('items', []):
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            videos.append(f"- [Video] {title}: https://www.youtube.com/watch?v={video_id}")
        return videos
    except HttpError as e:
        # Handle API errors gracefully
        print(f"An HTTP error occurred while calling YouTube API: {e}", file=sys.stderr)
        return [f"Error: Could not fetch YouTube videos. Check API key and quota."]

def find_articles(topic: str, max_results: int = 2) -> list:
    """Finds top web articles/tutorials for a given topic."""
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_SEARCH_API_KEY)
        search_query = f"in-depth tutorial {topic}"

        res = service.cse().list(q=search_query, cx=SEARCH_ENGINE_ID, num=max_results).execute()

        articles = []
        for item in res.get('items', []):
            title = item['title']
            link = item['link']
            articles.append(f"- [Article] {title}: {link}")
        return articles
    except HttpError as e:
        print(f"An HTTP error occurred while calling Google Search API: {e}", file=sys.stderr)
        return [f"Error: Could not fetch articles. Check API key and quota."]

def find_resources(topic: str) -> list:
    """Fetches both videos and articles for a given topic."""
    # Check if the API keys are loaded
    if not all([YOUTUBE_API_KEY, GOOGLE_SEARCH_API_KEY, SEARCH_ENGINE_ID]):
        return ["Error: API keys are not configured correctly in the deployment environment."]

    videos = find_youtube_videos(topic)
    articles = find_articles(topic)

    return videos + articles
