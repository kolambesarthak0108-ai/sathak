# 🎓 CampusMind AI – Intelligent Academic & College Assistant Chatbot

> **VITyarthi "Build Your Own Project" Evaluation Project**  
> An NLP-powered, multi-turn conversational AI web application designed for students and faculty.

---

## 🌟 1. Project Overview
**CampusMind AI** is an intelligent academic chatbot designed to streamline information access in higher education institutions. Using custom Natural Language Processing (NLP) tokenization, TF-IDF vectorization, cosine similarity classification, and contextual dialogue state tracking, CampusMind AI assists students with:
- Course catalogs and module-by-module syllabus details
- Midterm and final examination schedules
- 10-point CGPA grading scales and 75% attendance policies
- Faculty directories and cabin locations
- Campus facilities, library timings, and hostel policies
- Hands-free voice speech input and audio read-aloud

---

## ✨ 2. Key Features
- **Intelligent Intent Recognition:** 12 trained intent categories with dynamic confidence scoring and fallback detection.
- **Academic Entity Extraction:** Recognizes course codes (e.g. `CS101`, `CS201`, `CS301`), semesters, and faculty names.
- **Multi-Turn Contextual Memory:** Remembers active course context across subsequent questions (e.g., asking *"Who is the teacher?"* after inquiring about *CS201*).
- **Modern Glassmorphic Web Interface:** Sleek responsive UI with dark/light themes, suggested query chips, and real-time typing indicators.
- **Voice-Enabled Speech Interface:** Native Web Speech API integration for hands-free voice dictation (STT) and audio response narration (TTS).
- **Live System Telemetry:** In-app metrics modal reporting query volume, response latency ($< 25\text{ ms}$), and user satisfaction.
- **Persistent SQLite Storage:** Durable storage for session logs, timestamps, user ratings, and telemetry metrics.
- **Built-in Academic Report:** Access the complete 15-section project report at `/report` with rendered Mermaid diagrams, ready for PDF export.

---

## 🛠️ 3. Technologies & Tools Used
- **Backend Language:** Python 3 (3.10+)
- **Web Framework:** Flask (REST API & routing)
- **Natural Language Processing:** Custom TF-IDF vectorizer, Tokenizer, Cosine Similarity Engine
- **Persistence:** SQLite3
- **Frontend:** Semantic HTML5, Vanilla CSS3 (Glassmorphism & CSS Variables), JavaScript (ES6+)
- **Speech APIs:** W3C Web Speech API (SpeechRecognition & SpeechSynthesis)
- **Automated Testing:** Pytest 8.x
- **Diagrams & Documentation:** Mermaid.js & GitHub Markdown

---

## 🚀 4. Steps to Install & Run the Project

### Prerequisites
- Python 3.10 or higher installed.

### Step 1: Clone or Navigate to the Project Directory
```bash
git clone https://github.com/your-username/vityarti.git
cd vityarti
```

### Step 2: Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### Step 3: Run the Application Server
```bash
python app.py
```

### Step 4: Open in Web Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

To view or print the comprehensive 15-section academic project report, visit:
```
http://127.0.0.1:5000/report
```

---

## 🧪 5. Instructions for Testing
The project includes a comprehensive automated test suite covering text normalization, intent classification, entity extraction, knowledge retrieval, and REST API routes.

Run the test suite using `pytest`:
```bash
python -m pytest tests/ -v
```

Expected output:
```
tests/test_preprocessor.py::test_clean_and_tokenize PASSED
tests/test_preprocessor.py::test_stopwords_and_intent_words PASSED
tests/test_intent.py::test_greeting_intent PASSED
tests/test_intent.py::test_course_and_syllabus_intent PASSED
tests/test_intent.py::test_fallback_intent PASSED
tests/test_knowledge.py::test_get_course PASSED
tests/test_knowledge.py::test_get_policy PASSED
tests/test_api.py::test_chat_endpoint PASSED
tests/test_api.py::test_analytics_endpoint PASSED
```

---

## 📁 6. Project Directory Structure
```
vityarti/
├── app.py                     # Flask Server & REST API endpoints
├── requirements.txt           # Python dependencies
├── statement.md               # VITyarthi Problem Statement & Scope (Sec 5.2)
├── README.md                  # Project overview, installation, testing (Sec 5.1)
├── campusmind.db              # SQLite persistent database (auto-generated)
│
├── nlp/                       # Functional Module 1: NLP Pipeline
│   ├── __init__.py
│   ├── preprocessor.py        # Tokenizer, normalizer, stopword filter
│   ├── intent_classifier.py   # TF-IDF & Cosine Similarity intent engine
│   └── entity_extractor.py    # Academic entity recognition
│
├── core/                      # Functional Module 2: Dialogue & Knowledge
│   ├── __init__.py
│   ├── knowledge_base.py      # Syllabi, faculty, timetable repository
│   ├── dialogue_manager.py    # Context retention & response generation
│   └── analytics.py           # Latency and telemetry tracker
│
├── models/                    # Functional Module 3: Storage & Persistence
│   ├── __init__.py
│   └── database.py            # SQLite schema, interactions, and feedback logs
│
├── static/                    # Frontend Assets
│   ├── css/
│   │   └── style.css          # Glassmorphism, animations, responsive styling
│   └── js/
│       └── app.js             # Client controller, Web Speech API, themes
│
├── templates/                 # Web Views
│   ├── index.html             # Semantic Chatbot Web Interface
│   └── report.html            # 15-Section Academic Project Report with Mermaid
│
├── report/
│   └── PROJECT_REPORT.md      # Markdown version of 15-section report
│
└── tests/                     # Automated Test Suite
    ├── test_preprocessor.py
    ├── test_intent.py
    ├── test_knowledge.py
    └── test_api.py
```

---

## 📜 7. License & Academic Attribution
Developed as an original project submission for the **VITyarthi "Build Your Own Project"** evaluation.  
All academic code and documentation adhere to the prescribed submission rubrics.
