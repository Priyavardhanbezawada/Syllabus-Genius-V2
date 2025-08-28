# app.py
from flashcard_generator import generate_flashcards
from concept_mapper import generate_concept_map
from flask import Flask, request, render_template, url_for, session, redirect
import os
from werkzeug.utils import secure_filename
import urllib.parse

# Import all your helper modules
from pdf_parser import extract_text
from topic_extractor import extract_topics
from resource_finder import find_resources
from content_generator import generate_explanation
from quiz_generator import generate_quiz

app = Flask(__name__)
# A secret key is needed to keep track of the user's quiz session
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Main Page: Handles file upload and shows topic list ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Clear any old session data when a new file is uploaded
        session.clear()
        file = request.files.get('file')
        if not file or file.filename == '':
            return render_template('index.html', error="No file selected.")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            raw_text = extract_text(filepath)
            topics = extract_topics(raw_text)
            # Store topics in the session to use them across pages
            session['topics'] = topics
            concept_map_html = generate_concept_map(topics)
            session['concept_map'] = concept_map_html
        finally:
            os.remove(filepath)

        if not topics:
            return render_template('index.html', error="Could not extract topics.")

        return render_template('index.html', topics=topics)

    # On a GET request, show topics if they are in the session
    return render_template('index.html', topics=session.get('topics'))

# --- Details Page: Shows content for a single topic ---
@app.route('/topic/<topic_name>')
def topic_details(topic_name):
    topic = urllib.parse.unquote_plus(topic_name)
    explanation = generate_explanation(topic)
    youtube_videos = find_resources(topic)
    return render_template('details.html', topic=topic, explanation=explanation, videos=youtube_videos)

# --- NEW: Quiz Start Page ---
@app.route('/quiz/start/<topic_name>')
def start_quiz(topic_name):
    topic = urllib.parse.unquote_plus(topic_name)
    # Generate the quiz and store it in the user's session
    quiz_data = generate_quiz(topic)
    session['quiz'] = quiz_data.get('quiz')
    session['current_question'] = 0
    session['score'] = 0
    session['topic'] = topic

    if not session['quiz']:
         # Handle error if quiz generation fails
        return render_template('index.html', topics=session.get('topics'), error=quiz_data.get("error"))

    # Redirect to the first question
    return redirect(url_for('show_question'))

# --- NEW: Quiz Question Page ---
@app.route('/quiz/question', methods=['GET', 'POST'])
def show_question():
    question_index = session.get('current_question', 0)
    quiz = session.get('quiz')

    if not quiz or question_index >= len(quiz):
        # If quiz is over, go to results
        return redirect(url_for('quiz_results'))

    question_data = quiz[question_index]

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = question_data['answer']

        # Check if the answer is correct and update score
        if user_answer and user_answer.lower() == correct_answer.lower():
            session['score'] = session.get('score', 0) + 10 # 10 points per correct answer

        # Move to the next question
        session['current_question'] = question_index + 1
        return redirect(url_for('show_question'))

    return render_template('quiz.html', question=question_data, q_index=question_index, total_questions=len(quiz))

# --- NEW: Quiz Results Page ---
@app.route('/quiz/results')
def quiz_results():
    score = session.get('score', 0)
    total_questions = len(session.get('quiz', []))
    topic = session.get('topic', 'your quiz')

    badge = None
    # Badge System Logic
    if total_questions > 0:
        percentage = (score / (total_questions * 10)) * 100
        if percentage == 100:
            badge = {"name": "Topic Master 🏆", "desc": "Perfect score! You've mastered this topic."}
        elif percentage >= 70:
            badge = {"name": "Expert Learner 🥇", "desc": "Excellent work! You have a strong grasp of the material."}
        elif percentage >= 50:
            badge = {"name": "Solid Foundation 🥈", "desc": "Good job! Keep reviewing to solidify your knowledge."}

    return render_template('results.html', score=score, total=total_questions * 10, topic=topic, badge=badge)

# --- NEW: Flashcards Page ---
# --- NEW: Flashcards Page (More Robust) ---
@app.route('/flashcards/<topic_name>')
def show_flashcards(topic_name):
    topic = urllib.parse.unquote_plus(topic_name)
    flashcard_data = generate_flashcards(topic)

    # --- FIX: Check for errors AND the correct data structure ---
    if "error" in flashcard_data or "flashcards" not in flashcard_data or not isinstance(flashcard_data.get('flashcards'), list):
        error_message = flashcard_data.get("error", "An unknown error occurred while generating flashcards.")
        # Redirect to the main page with a clear error message
        return render_template('index.html', topics=session.get('topics'), error=error_message)

    # If everything is okay, show the flashcards
    return render_template('flashcards.html', topic=topic, flashcards=flashcard_data['flashcards'])


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)))
