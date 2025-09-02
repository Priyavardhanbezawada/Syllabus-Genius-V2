# Syllabus Genius V2 📚

An AI-powered educational web application that transforms syllabus documents and study materials into interactive learning experiences. Upload PDFs or images of your syllabus, and get automatically generated topic breakdowns, detailed explanations, flashcards, and quizzes.

## ✨ Features

### 📄 Document Processing
- **PDF Support**: Extract text from PDF documents using PyMuPDF
- **Image Support**: OCR text extraction from images using EasyOCR and Pillow
- **Smart Parsing**: Intelligent document analysis and topic extraction

### 🤖 AI-Powered Learning Tools
- **Topic Extraction**: Automatically identify key concepts and topics from documents using Groq AI
- **Content Generation**: Generate comprehensive explanations for each topic
- **Flashcard Creation**: Auto-generate flashcards for effective memorization
- **Quiz Generation**: Create interactive quizzes with scoring and badges
- **Resource Finding**: Discover relevant YouTube videos and learning resources

### 🎯 Interactive Learning Experience
- **Topic Navigation**: Browse extracted topics with detailed explanations
- **Flashcard System**: Interactive flashcard interface for self-study
- **Quiz Engine**: Progressive quiz system with scoring and achievement badges
- **Badge System**: Earn badges based on quiz performance:
  - 🏆 **Topic Master**: Perfect score (100%)
  - 🥇 **Expert Learner**: Excellent performance (70%+)
  - 🥈 **Solid Foundation**: Good performance (50%+)

### 🌐 Web Interface
- **Responsive Design**: Clean, user-friendly web interface
- **Session Management**: Maintain user progress across quiz sessions
- **File Upload**: Secure file handling with automatic cleanup
- **Real-time Processing**: Fast document processing and content generation

## 🛠️ Technology Stack

### Backend
- **Flask**: Lightweight Python web framework
- **Gunicorn**: WSGI HTTP Server for deployment
- **Werkzeug**: Web application library for secure file handling

### AI & Machine Learning
- **Groq API**: Advanced language model for content generation
- **EasyOCR**: Optical Character Recognition for image processing
- **PyTorch**: Deep learning framework supporting OCR operations

### Document Processing
- **PyMuPDF**: PDF text extraction and processing
- **Pillow (PIL)**: Image processing and manipulation
- **python-dotenv**: Environment variable management

### External APIs
- **Google APIs**: YouTube video search and resource discovery
  - `google-api-python-client`
  - `google-auth-oauthlib`
  - `google-auth-httplib2`

### Additional Libraries
- **Markdown**: Text formatting and rendering
- **ics**: Calendar integration support

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Groq API key
- Google API credentials (for YouTube integration)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Priyavardhanbezawada/Syllabus-Genius-V2.git
   cd Syllabus-Genius-V2
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Create uploads directory**:
   ```bash
   mkdir uploads
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:8080`

## 📖 Usage

### Getting Started
1. **Upload Document**: Navigate to the home page and upload a PDF or image file containing your syllabus
2. **View Topics**: The AI will automatically extract key topics from your document
3. **Explore Content**: Click on any topic to view detailed explanations and resources
4. **Study Tools**: Use the flashcards and quiz features for each topic

### Features Walkthrough

#### Topic Details
- Click on any extracted topic to view:
  - Comprehensive AI-generated explanations
  - Relevant YouTube video resources
  - Links to flashcards and quizzes

#### Flashcards
- Interactive flashcard interface
- Navigate through cards for effective memorization
- Perfect for quick review sessions

#### Quizzes
- Multiple-choice questions generated for each topic
- Real-time scoring system
- Achievement badges based on performance
- Progress tracking across sessions

## 🏗️ Project Structure

```
Syllabus-Genius-V2/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── templates/               # HTML templates
│   └── quiz.html           # Quiz interface template
├── pdf_parser.py           # PDF text extraction
├── image_parser.py         # Image OCR processing
├── topic_extractor.py      # AI-powered topic extraction
├── content_generator.py    # Content generation using AI
├── quiz_generator.py       # Quiz creation logic
├── flashcard_generator.py  # Flashcard generation
├── resource_finder.py      # YouTube resource discovery
├── concept_mapper.py       # Concept relationship mapping
└── uploads/                # Temporary file storage
```

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: Required for AI content generation
- `GOOGLE_API_KEY`: Required for YouTube resource discovery
- `PORT`: Application port (default: 8080)

### File Upload Settings
- Supported formats: PDF, PNG, JPG, JPEG
- Maximum file size: Configurable via Flask settings
- Automatic file cleanup after processing

## 🚀 Deployment

The application is configured for deployment on platforms like Render, Heroku, or similar:

1. Set environment variables in your deployment platform
2. The application automatically uses `PORT` environment variable
3. Gunicorn is included for production serving

### Render Deployment
```bash
# The app will automatically start with:
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Priyavardhanbezawada**
- GitHub: [@Priyavardhanbezawada](https://github.com/Priyavardhanbezawada)

## 🙏 Acknowledgments

- **Groq AI** for providing the language model API
- **Google** for YouTube API integration
- **EasyOCR** for optical character recognition
- **Flask** community for the excellent web framework

## 📊 Project Stats

- **Language**: Python (69.7%), HTML (30.3%)
- **Framework**: Flask
- **AI Integration**: Groq API
- **Document Processing**: PDF + Image support
- **Features**: 6 core modules, Interactive UI

---

*Transform your learning experience with AI-powered study tools! 🎓*
