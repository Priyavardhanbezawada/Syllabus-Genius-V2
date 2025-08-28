# app.py
from flask import Flask, request, render_template, url_for
import os
from werkzeug.utils import secure_filename
import urllib.parse

# Import all your helper modules
from pdf_parser import extract_text
from topic_extractor import extract_topics
from resource_finder import find_resources
from content_generator import generate_explanation

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Main Page: Handles file upload and shows topic list ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return render_template('index.html', error="No file selected.")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            raw_text = extract_text(filepath)
            topics = extract_topics(raw_text)
        finally:
            os.remove(filepath)

        if not topics:
            return render_template('index.html', error="Could not extract topics from the document.")

        # Instead of results, just pass the list of topics
        return render_template('index.html', topics=topics)

    return render_template('index.html', topics=None)

# --- Details Page: Shows content for a single topic ---
@app.route('/topic/<topic_name>')
def topic_details(topic_name):
    # Decode the topic name from the URL
    topic = urllib.parse.unquote_plus(topic_name)

    # --- Fetch all content for this topic ---
    # 1. Generate the exam-focused explanation
    explanation = generate_explanation(topic)

    # 2. Find the YouTube videos
    youtube_videos = find_resources(topic)

    # Send all the data to a new HTML template
    return render_template('details.html', topic=topic, explanation=explanation, videos=youtube_videos)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)))
