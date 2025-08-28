# app.py
from flask import Flask, request, render_template, url_for, session, redirect
import os
from werkzeug.utils import secure_filename
import urllib.parse

# Import all your helper modules
from pdf_parser import extract_text
from image_parser import extract_text_from_image
from topic_extractor import extract_topics
from resource_finder import find_resources
from content_generator import generate_explanation
from quiz_generator import generate_quiz
from flashcard_generator import generate_flashcards

app = Flask(__name__)
# A secret key is needed to manage user sessions for quizzes
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Main Page: Handles file upload and shows topic list ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.clear() # Clear old data on new upload
        file = request.files.get('file')
        if not file or file.filename == '':
            return render_template('index.html', error="No file selected.")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        raw_text = ""
        try:
            if filename.lower().endswith('.pdf'):
                raw_text = extract_text(filepath)
            else:
                with open(filepath, 'rb') as f:
                    image_bytes = f.read()
                raw_text = extract_text_from_image(image_bytes)
            
            topics = extract_topics(raw_text)
            session['topics'] = topics
        finally:
            os.remove(filepath)

        if not topics:
            return render_template('index.html', error="Could not extract topics from the document.")
        
        return render_template('index.html', topics=topics)

    return render_template('index.html', topics=session.get('topics'))

# --- Details Page: Shows content for a single topic ---
@app.route('/topic/<topic_name>')
def topic_details(topic_name):
    topic = urllib.parse.unquote_plus(topic_name)
    explanation = generate_explanation(topic)
    youtube_videos = find_resources(topic)
    return render_template('details.html', topic=topic, explanation=explanation, videos=youtube_videos)

# --- Flashcards Page ---
@app.route('/flashcards/<topic_name>')
def show_flashcards(topic_name):
    topic = urllib.parse.unquote_plus(topic_name)
    flashcard_data = generate_flashcards(topic)
    if "error" in flashcard_data or not flashcard_data.get('flashcards'):
        error_message = flashcard_data.get("error", "Failed to generate flashcards.")
        return render_template('index.html', topics=session.get('topics'), error=error_message)
    return render_template('flashcards.html', topic=topic, flashcards=flashcard_data['flashcards'])

# --- Quiz Start Page ---
@app.route('/quiz/start/<topic_name>')
def start_quiz(topic_name):
    topic = urllib.parse.unquote_plus(topic_name)
    quiz_data = generate_quiz(topic)
    if "error" in quiz_data or not quiz_data.get('quiz'):
        error_message = quiz_data.get("error", "Failed to generate a quiz for this topic.")
        return render_template('index.html', topics=session.get('topics'), error=error_message)
    
    session['quiz'] = quiz_data['quiz']
    session['current_question'] = 0
    session['score'] = 0
    session['topic'] = topic
    return redirect(url_for('show_question'))

# --- Quiz Question Page ---
@app.route('/quiz/question', methods=['GET', 'POST'])
def show_question():
    question_index = session.get('current_question', 0)
    quiz = session.get('quiz')
    if not quiz or question_index >= len(quiz):
        return redirect(url_for('quiz_results'))

    question_data = quiz[question_index]
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = question_data['answer']
        if user_answer and user_answer.lower() == correct_answer.lower():
            session['score'] = session.get('score', 0) + 10
        session['current_question'] = question_index + 1
        return redirect(url_for('show_question'))

    return render_template('quiz.html', question=question_data, q_index=question_index, total_questions=len(quiz))

# --- Quiz Results Page ---
@app.route('/quiz/results')
def quiz_results():
    score = session.get('score', 0)
    total_questions = len(session.get('quiz', []))
    topic = session.get('topic', 'your quiz')
    
    badge = None
    if total_questions > 0:
        percentage = (score / (total_questions * 10)) * 100
        if percentage == 100:
            badge = {"name": "Topic Master 🏆", "desc": "Perfect score! You've mastered this topic."}
        elif percentage >= 70:
            badge = {"name": "Expert Learner 🥇", "desc": "Excellent work! You have a strong grasp of the material."}
        elif percentage >= 50:
            badge = {"name": "Solid Foundation 🥈", "desc": "Good job! Keep reviewing to solidify your knowledge."}

    return render_template('results.html', score=score, total=total_questions * 10, topic=topic, badge=badge)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)))
