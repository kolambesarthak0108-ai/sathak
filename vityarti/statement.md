# Problem Statement & Project Scope

## Project Title
**CampusMind AI – Intelligent Academic & College Assistant Chatbot**

## 1. Problem Statement
Academic institutions possess extensive repositories of curricula, examination regulations, grading metrics, and administrative contacts. However, this information is typically scattered across disparate web portals, static PDF handbooks, and physical notice boards. As a result:
- Students spend excessive time locating essential details such as syllabus breakdowns, course prerequisites, exam dates, and CGPA formulas.
- Faculty and administrative staff face constant, repetitive inquiries that divert time from instruction and research.
- Support is unavailable outside regular office hours when students are studying for tests or preparing course registrations.

**CampusMind AI** resolves this problem by offering a 24/7 intelligent conversational chatbot that parses natural language questions, extracts academic entities, retains conversational context, and delivers immediate, accurate responses with voice dictation and read-aloud capabilities.

## 2. Scope of the Project
The scope of the project encompasses:
- **Curriculum & Academic Advisory:** Delivering course credits, prerequisites, module-by-module syllabi, and lecture timings for computer science and engineering disciplines.
- **Examination & Assessment Intelligence:** Providing examination schedules (CAT-1, CAT-2, FAT, Lab exams), hall ticket release dates, and evaluation weightages.
- **Academic Policy Guidance:** Clarifying the 10-point relative/absolute grading scale, passing criteria, and the mandatory 75% attendance threshold.
- **Faculty Directory Assistance:** Assisting students with instructor email addresses, department heads, office locations, and consultation timings.
- **Campus Life & Facilities Support:** Answering questions on central library hours, borrowing limits, hostel curfew regulations, and dining timings.
- **Multi-Turn Contextual Awareness:** Preserving the active course context across conversational turns to handle natural follow-up inquiries.
- **Speech Interaction & Telemetry:** Supporting browser-based Speech-to-Text input, Text-to-Speech playback, and logging real-time performance latency and user satisfaction metrics.

## 3. Target Users
1. **Undergraduate & Postgraduate Students:** Seeking fast, accessible answers regarding subjects, exam schedules, course modules, faculty contacts, and college regulations.
2. **Prospective & New Students:** Navigating campus policies, syllabus structures, facilities, and academic requirements.
3. **Faculty & Academic Advisors:** Reducing repetitive administrative inquiries so they can concentrate on high-impact mentorship.
4. **Academic Evaluators & Administrators:** Reviewing real-time system performance, query distributions, and student satisfaction through built-in telemetry metrics.

## 4. High-Level Features
- **Natural Language Intent Recognition:** TF-IDF vectorization and Cosine Similarity classification capable of detecting 12 distinct conversational intents.
- **Academic Entity Extraction:** Automatically identifies course codes (e.g., `CS101`, `CS201`, `CS301`), semester identifiers, faculty aliases, and exam categories.
- **Context-Aware Dialogue Manager:** Remembers conversational entities across dialogue turns for natural multi-turn interactions.
- **Interactive Modern Web Interface:** Dark/light mode theme toggle, glassmorphism UI, suggested question chips, and live typing indicators.
- **Voice Speech Integration:** Native Speech-to-Text dictation and Text-to-Speech response reading using the Web Speech API.
- **Performance Telemetry Dashboard:** Tracks query count, average response latency, and thumbs up/down user feedback in an SQLite database.
- **Academic Submission Suite:** Built-in 15-section printable project report and automated test suite.
