# resource_finder.py
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys

# This will load the secret API key you have set on Render.
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def find_resources(topic: str, max_results: int = 3) -> list:
    """
    Finds the top YouTube video tutorials for a given topic.
    """
    # First, check if the API key was successfully loaded from the environment.
    if not YOUTUBE_API_KEY:
        return ["Error: YOUTUBE_API_KEY is not configured in the environment."]

    try:
        # Build the YouTube service object
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        # Create a specific search query for better results
        search_query = f"{topic} tutorial explained"

        # Execute the search request
        request = youtube.search().list(
            q=search_query,
            part='snippet',
            maxResults=max_results,
            type='video',
            relevanceLanguage='en'
        )
        response = request.execute()

        videos = []
        # Parse the response to get the video title and link
        for item in response.get('items', []):
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            # Format the result as a clean Markdown link
            videos.append(f"- [Video] {title}: https://www.youtube.com/watch?v={video_id}")

        if not videos:
            return ["No relevant YouTube videos found for this topic."]

        return videos

    except HttpError as e:
        # Handle potential API errors, like an invalid key or exceeded quota
        print(f"An HTTP error occurred while calling the YouTube API: {e}", file=sys.stderr)
        return ["Error: Could not fetch YouTube videos. Please check the API key and your quota in the Google Cloud Console."]
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return ["An unexpected error occurred while searching for resources."]
