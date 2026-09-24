# Project Report: CampusMind AI – Intelligent Academic & College Chatbot

**Course:** VITyarthi - Build Your Own Project (Flipped Course Evaluation)  
**Project Title:** CampusMind AI Academic Assistant  
**Domain:** Artificial Intelligence / Natural Language Processing / Web Development  
**Submission Year:** 2026  

---

## 1. Introduction
In university environments, students often face hurdles retrieving accurate and timely information regarding courses, syllabi, exam schedules, and grading standards. **CampusMind AI** is an intelligent conversational agent engineered to provide 24/7 automated academic assistance using Natural Language Processing (NLP), multi-turn dialogue management, and modern web technologies.

---

## 2. Problem Statement
Academic data is distributed across diverse documents and portals, creating significant inquiry overhead for campus faculty and staff while delaying urgent answers for students. The goal of this project is to build an automated, reliable, and user-friendly AI Chatbot capable of understanding conversational queries, providing structured answers, remembering context across turns, and facilitating speech-based interaction.

---

## 3. Functional Requirements (FR)
The application comprises three core functional modules:
1. **NLP & Intent Classification Engine (Module 1):**
   - Text preprocessing, sanitization, tokenization, and stopword filtering.
   - TF-IDF vectorization and Cosine Similarity classification over 12 intent categories.
   - Academic entity recognition (Course codes, semesters, faculty names, exam types).
2. **Dialogue & Knowledge Management (Module 2):**
   - Multi-turn context tracking (persisting active course across turns).
   - Knowledge retrieval across course syllabi, exam timetables, GPA grading policies, and campus amenities.
   - Fallback keyword search and intelligent suggestion generation.
3. **Web Presentation & Telemetry (Module 3):**
   - Responsive modern chat interface with dark/light themes.
   - Voice dictation (Speech-to-Text) and text-to-speech audio reading via Web Speech API.
   - Real-time telemetry monitoring (latency, query count, user feedback).

---

## 4. Non-Functional Requirements (NFR)
1. **Performance:** Query classification and response generation latency $\le 150\text{ ms}$.
2. **Usability & Accessibility:** Clean interface with high visual aesthetics, mobile responsiveness, and voice accessibility.
3. **Reliability & Robustness:** Graceful fallback for uncataloged queries ($< 0.22$ confidence score) with helpful topic prompts.
4. **Maintainability & Modularity:** Adheres to modular separation of concerns with automated test coverage.

---

## 5. System Architecture
```mermaid
graph TD
    Client["Client Web Interface (HTML5/CSS3/JS/Web Speech)"]
    API["Flask REST API Server (app.py)"]
    DM["Dialogue Manager (core/dialogue_manager.py)"]
    NLP["NLP Pipeline (preprocessor, classifier, extractor)"]
    KB["Knowledge Base (core/knowledge_base.py)"]
    DB[("SQLite Storage (campusmind.db)")]
    Telemetry["Analytics Tracker (core/analytics.py)"]

    Client -->|HTTP POST /api/chat| API
    Client -->|HTTP GET /api/analytics| API
    API --> DM
    DM --> NLP
    DM --> KB
    DM --> DB
    API --> Telemetry
    API --> Client
```

---

## 6. Design Diagrams

### 6.1 Use Case Diagram
```mermaid
flowchart LR
    Student((Student / User))
    Evaluator((Evaluator / Admin))

    subgraph CampusMind_System["CampusMind AI System"]
        UC1[Inquire Course Syllabus]
        UC2[Check Exam Schedule]
        UC3[View Grading & Attendance Policy]
        UC4[Contact Faculty Directory]
        UC5[Use Voice Dictation / Speech Output]
        UC6[Submit Thumbs Up/Down Feedback]
        UC7[View System Telemetry & Metrics]
        UC8[View Academic Project Report]
    end

    Student --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC4
    Student --> UC5
    Student --> UC6

    Evaluator --> UC7
    Evaluator --> UC8
```

### 6.2 Workflow / Flowchart Diagram
```mermaid
flowchart TD
    Start([User Input Received]) --> Tokenize[Clean & Tokenize Text]
    Tokenize --> IntentScore[Compute TF-IDF Vector & Cosine Similarity]
    IntentScore --> CheckConf{Confidence >= 0.22?}

    CheckConf -- Yes --> ExtractEntities[Extract Academic Entities]
    CheckConf -- No --> KeywordSearch[Scan KB for Curriculum Keywords]

    KeywordSearch --> FoundMatches{Matches Found?}
    FoundMatches -- Yes --> BuildSuggest[Formulate Suggested Course Topics]
    FoundMatches -- No --> FallbackResponse[Provide General Help & Quick Chips]

    ExtractEntities --> UpdateContext[Update Session Active Context]
    UpdateContext --> QueryKB[Retrieve Academic Syllabus / Details]
    QueryKB --> FormatResponse[Generate Markdown Response]

    BuildSuggest --> FormatResponse
    FallbackResponse --> FormatResponse
    FormatResponse --> LogInteraction[Persist to SQLite & Measure Latency]
    LogInteraction --> Deliver[Deliver JSON to Web Client]
    Deliver --> End([Render Bubble & Suggestions])
```

### 6.3 Sequence Diagram
```mermaid
sequenceDiagram
    autonumber
    actor User as Student
    participant Web as Web Client
    participant Server as Flask Server
    participant DM as Dialogue Manager
    participant NLP as NLP Engine
    participant KB as Knowledge Base
    participant DB as SQLite DB

    User->>Web: Type / Speak Query
    Web->>Server: POST /api/chat {message, session_id}
    Server->>DM: process_message(session_id, message)
    DM->>NLP: predict(message) & extract(message)
    NLP-->>DM: {intent, confidence, entities}
    DM->>DM: update_context(entities)
    DM->>KB: get_course() / get_policy()
    KB-->>DM: academic_data
    DM-->>Server: synthesized_response
    Server->>DB: log_interaction(...)
    Server-->>Web: 200 OK JSON {response, suggestions, latency_ms}
    Web->>User: Display message + Speech synthesis
```

### 6.4 Class Diagram
```mermaid
classDiagram
    class TextPreprocessor {
        +clean(text: str) str
        +tokenize(text: str) List~str~
        +get_ngrams(tokens, n) List~str~
    }

    class IntentClassifier {
        -vocabulary: Dict
        -idf: Dict
        -intent_vectors: Dict
        +train(data) void
        +predict(text) Tuple~str, float~
    }

    class EntityExtractor {
        +extract(text) Dict
    }

    class KnowledgeBase {
        +get_course(code) Dict
        +get_syllabus(code) List
        +get_policy(topic) Dict
    }

    class DialogueManager {
        +process_message(session_id, message) Dict
    }

    class DatabaseManager {
        +log_interaction() int
        +save_feedback() int
        +get_session_history() List
    }

    DialogueManager --> IntentClassifier
    DialogueManager --> EntityExtractor
    DialogueManager --> KnowledgeBase
    IntentClassifier --> TextPreprocessor
```

### 6.5 Database ER Diagram
```mermaid
erDiagram
    SESSIONS ||--o{ CHAT_LOGS : contains
    SESSIONS ||--o{ FEEDBACK : records

    SESSIONS {
        string session_id PK
        float created_at
        float last_active
        string metadata
    }

    CHAT_LOGS {
        integer id PK
        string session_id FK
        float timestamp
        string user_message
        string bot_response
        string intent
        float confidence
        float latency_ms
    }

    FEEDBACK {
        integer id PK
        string session_id FK
        string rating
        string comment
        float timestamp
    }
```

---

## 7. Design Decisions & Rationale
1. **Lightweight TF-IDF vs. Heavy Transformer:** A custom TF-IDF classifier enables $<25\text{ ms}$ inference times on any machine without multi-gigabyte GPU or external cloud dependencies.
2. **Context-Driven Carry-over:** Enables conversation continuity when users ask follow-up questions (e.g. asking "Who teaches it?" after inquiring about CS201).
3. **Standard SQLite Storage:** Provides ACID transactional persistence without requiring external database servers.

---

## 8. Implementation Details
The project is organized into modular packages:
- `nlp/`: Text preprocessing, vectorization, intent matching, entity extraction.
- `core/`: Knowledge repository, multi-turn state management, telemetry.
- `models/`: SQLite schema, interaction logging, feedback persistence.
- `static/` & `templates/`: Modern glassmorphic web interface with Web Speech STT/TTS.
- `tests/`: Automated unit tests covering all modules.

---

## 9. Verification & Results
- All unit tests pass with 100% success rate.
- Response latency verified at $< 25\text{ ms}$.
- Context retention verified across consecutive turns.

---

## 10. Testing Approach
Unit testing with `pytest` covering:
- Text sanitization and token filtering.
- Intent classification accuracy and fallback threshold verification.
- Knowledge base query correctness.
- REST API response status and schema validation.

---

## 11. Challenges Faced
- Managing pronouns in multi-turn dialogues was solved by maintaining an active course context variable in the session state.
- Handling ambiguous user utterances was addressed using combined cosine similarity thresholds and curriculum fallback search.

---

## 12. Learnings & Key Takeaways
- Practical application of NLP preprocessing and vector space models.
- Dialogue management design patterns for conversational continuity.
- Building accessible web applications with modern styling and assistive voice technology.

---

## 13. Future Enhancements
- Multilingual translation support for regional languages.
- Integration with campus ERP / LMS systems for personalized marks and attendance.
- Document Q&A using Retrieval-Augmented Generation (RAG).

---

## 14. References
1. Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing*.
2. Flask Web Framework Documentation (<https://flask.palletsprojects.com/>).
3. W3C Web Speech API (<https://wicg.github.io/speech-api/>).
4. VITyarthi Project Guidelines & Rubric (2026).
