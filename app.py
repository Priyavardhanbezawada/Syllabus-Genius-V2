# app.py
from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename

# In the next steps, we will create these two Python helper files.
# For now, we are just importing them so our main app is ready.
from pdf_parser import extract_text
from topic_extractor import extract_topics

# Initialize the Flask application
app = Flask(__name__)

# Configure a temporary folder to store uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# This function will handle requests to our main webpage
@app.route('/', methods=['GET', 'POST'])
def index():
    # This block runs when the user uploads a file (a "POST" request)
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        
        file = request.files['file']
        
        if file.filename == '':
            return "No selected file", 400

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # --- This is where your Python logic runs ---
            try:
                # 1. Call your first Python helper to read the PDF
                raw_text = extract_text(filepath)
                
                # 2. Call your second Python helper to find the topics
                topics = extract_topics(raw_text)
            finally:
                # 3. Clean up by deleting the temporary file
                os.remove(filepath)
            
            # 4. Send the results to the HTML page to be displayed
            return render_template('index.html', topics=topics)

    # This runs when the user first visits the page (a "GET" request)
    # It just shows the initial upload page.
    return render_template('index.html', topics=None)

# This part is needed for the server to run
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)))
