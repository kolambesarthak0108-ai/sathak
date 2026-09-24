"""
Module: core.dialogue_manager
Purpose: Context retention, multi-turn state tracking, and conversational response generation.
"""
from typing import Dict, Any, Optional, List
from nlp.intent_classifier import IntentClassifier
from nlp.entity_extractor import EntityExtractor
from .knowledge_base import KnowledgeBase


class DialogueManager:
    """Orchestrates dialogue state, context carry-over, and response synthesis."""

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.knowledge_base = KnowledgeBase()
        # In-memory session store: session_id -> context dict
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def get_or_create_session(self, session_id: str) -> Dict[str, Any]:
        """Retrieve existing session context or initialize a fresh one."""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "turn_count": 0,
                "last_intent": None,
                "active_course": None,
                "active_semester": None,
                "history": []
            }
        return self.sessions[session_id]

    def process_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """
        Process user input, maintain context, retrieve information, and return formatted response.
        """
        session = self.get_or_create_session(session_id)
        session["turn_count"] += 1

        # 1. Check for specific knowledge search queries (projects, concepts, career guidance)
        search_match = self.knowledge_base.search_knowledge(message)
        if search_match.get("type") in ["project_ideas", "technical_concept", "study_guidance"]:
            intent = "knowledge_search"
            confidence = 0.95
        else:
            # Classify Intent with NLP Classifier
            intent, confidence = self.intent_classifier.predict(message)

        # 2. Extract Entities
        entities = self.entity_extractor.extract(message)

        # 3. Context Update / Carry-over
        if entities.get("course_code"):
            session["active_course"] = entities["course_code"]
        if entities.get("semester"):
            session["active_semester"] = entities["semester"]

        # 4. Generate Response based on Intent & Context
        response_text, suggestions, cards = self._generate_response(intent, confidence, entities, session, message)

        # 5. Update session history
        session["last_intent"] = intent
        interaction = {
            "turn": session["turn_count"],
            "user_message": message,
            "bot_response": response_text,
            "intent": intent,
            "confidence": confidence,
            "entities": entities
        }
        session["history"].append(interaction)

        return {
            "session_id": session_id,
            "response": response_text,
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "suggestions": suggestions,
            "cards": cards,
            "turn_count": session["turn_count"]
        }

    def _generate_response(
        self,
        intent: str,
        confidence: float,
        entities: Dict[str, Any],
        session: Dict[str, Any],
        raw_message: str
    ) -> (str, List[str], List[Dict[str, Any]]):
        """Synthesize natural conversational answer with suggested follow-up chips."""
        suggestions = []
        cards = []

        # --- GREETING ---
        if intent == "greeting":
            text = (
                "Hello! 👋 I'm **CampusMind AI**, your college academic and campus assistant. "
                "I can help you with course details, syllabus modules, exam schedules, GPA policies, "
                "faculty contacts, and campus facilities. How can I assist you today?"
            )
            suggestions = ["View available courses", "Exam schedule", "Grading system", "Library hours"]
            return text, suggestions, cards

        # --- BOT IDENTITY ---
        if intent == "bot_identity":
            text = (
                "I am **CampusMind AI**, an intelligent conversational assistant developed for students and faculty. "
                "My core capabilities include:\n"
                "• **Academic Search:** Detailed syllabus, prerequisites, credit weightage, and schedules\n"
                "• **Campus Administration:** Exam dates, hall tickets, attendance & grading policies\n"
                "• **Faculty Directory:** Instructor details, office hours, and cabin locations\n"
                "• **Campus Facilities:** Library hours, hostel rules, Wi-Fi access, and fee deadlines"
            )
            suggestions = ["Show course list", "Attendance rules", "Exam timetable", "Contact faculty"]
            return text, suggestions, cards

        # --- GOODBYE ---
        if intent == "goodbye":
            text = "Goodbye! Best of luck with your studies and projects. Feel free to return anytime if you have questions! 🎓"
            return text, [], cards

        # --- APPRECIATION ---
        if intent == "appreciation":
            text = "You're very welcome! I'm always happy to help. Let me know if there's anything else you need. 😊"
            suggestions = ["Course details", "Exam schedule", "Campus facilities"]
            return text, suggestions, cards

        # --- COURSE INFO ---
        if intent == "course_info":
            target_course = entities.get("course_code") or session.get("active_course")
            if target_course:
                course_data = self.knowledge_base.get_course(target_course)
                if course_data:
                    text = (
                        f"### 📘 {course_data['code']}: {course_data['title']}\n\n"
                        f"• **Credits:** {course_data['credits']}\n"
                        f"• **Instructor:** {course_data['instructor']}\n"
                        f"• **Prerequisites:** {course_data['prerequisites']}\n"
                        f"• **Class Timing:** {course_data['schedule']}\n"
                        f"• **Evaluation Scheme:** {course_data['exam_weightage']}\n\n"
                        f"Would you like to review the complete module-by-module syllabus for {course_data['code']}?"
                    )
                    cards.append({
                        "type": "course_card",
                        "title": f"{course_data['code']} - {course_data['title']}",
                        "credits": course_data["credits"],
                        "timing": course_data["schedule"]
                    })
                    suggestions = [f"Syllabus for {course_data['code']}", "Who is the instructor?", "Exam schedule", "Back to all courses"]
                    return text, suggestions, cards

            # If no specific course mentioned, list all available courses
            courses = self.knowledge_base.get_all_courses()
            course_list_str = "\n".join([f"• **{c['code']}** – {c['title']} ({c['credits']} Credits, {c['instructor']})" for c in courses])
            text = (
                "Here are the active courses available in the curriculum:\n\n"
                f"{course_list_str}\n\n"
                "Ask me about any specific course code (e.g., *'Tell me about CS201'* or *'Syllabus for CS301'*)."
            )
            suggestions = ["Tell me about CS101", "Tell me about CS201", "Tell me about CS301", "Tell me about CS302"]
            return text, suggestions, cards

        # --- SYLLABUS INQUIRY ---
        if intent == "syllabus_inquiry":
            target_course = entities.get("course_code") or session.get("active_course")
            if not target_course:
                # Default to CS201 or prompt
                target_course = "CS201"
            course_data = self.knowledge_base.get_course(target_course)
            if course_data:
                modules_formatted = "\n".join([f"  {m}" for m in course_data["syllabus"]])
                text = (
                    f"### 📋 Syllabus Breakdown for **{course_data['code']} ({course_data['title']})**\n\n"
                    f"{modules_formatted}\n\n"
                    f"**Prerequisites:** {course_data['prerequisites']}\n"
                    f"**Evaluation:** {course_data['exam_weightage']}"
                )
                suggestions = [f"Instructor for {course_data['code']}", "Exam schedule", "Syllabus for CS301", "Grading criteria"]
                return text, suggestions, cards

        # --- EXAM SCHEDULE ---
        if intent == "exam_schedule":
            exam_info = self.knowledge_base.get_policy("exam_schedule")
            text = f"### 🗓️ {exam_info['summary']}\n\n{exam_info['details']}"
            suggestions = ["Grading policy", "Attendance requirement", "Library study hours"]
            return text, suggestions, cards

        # --- GRADING POLICY & ATTENDANCE ---
        if intent == "grading_policy":
            grade_info = self.knowledge_base.get_policy("grading_policy")
            text = f"### 📊 {grade_info['summary']}\n\n{grade_info['details']}"
            suggestions = ["When are final exams?", "Course syllabus", "Tuition fees"]
            return text, suggestions, cards

        # --- FACULTY CONTACT ---
        if intent == "faculty_contact":
            target_course = entities.get("course_code") or session.get("active_course")
            if target_course:
                course_data = self.knowledge_base.get_course(target_course)
                if course_data:
                    text = (
                        f"### 👨‍🏫 Instructor for **{course_data['code']}**\n\n"
                        f"**{course_data['instructor']}**\n"
                        f"• Course: {course_data['title']}\n"
                        f"• Office Hours: Prior appointment via email or after class hours."
                    )
                    suggestions = [f"Syllabus for {course_data['code']}", "Class timings", "Other faculty"]
                    return text, suggestions, cards

            # If general faculty inquiry
            text = (
                "### 👨‍🏫 Key Academic Faculty Contacts\n\n"
                "• **Dr. R. K. Sharma** – HOD Computer Science (Tech Block 301, `rksharma@campus.edu`)\n"
                "• **Prof. Ananya Verma** – AI & Machine Learning Lead (AI Lab 102, `averma@campus.edu`)\n"
                "• **Dr. Sunil Patel** – Programming & Web Tech (Tech Block 204, `spatel@campus.edu`)\n"
                "• **Prof. Priya Gupta** – Mathematics & Theoretical CS (Science Block 112, `pgupta@campus.edu`)\n\n"
                "Ask about a specific subject to see its assigned professor!"
            )
            suggestions = ["Who teaches CS201?", "Who teaches CS301?", "HOD contact details"]
            return text, suggestions, cards

        # --- LIBRARY SERVICES ---
        if intent == "library_services":
            lib_info = self.knowledge_base.get_policy("library_services")
            text = f"### 📚 {lib_info['summary']}\n\n{lib_info['details']}"
            suggestions = ["Campus Wi-Fi details", "Hostel timings", "Exam schedule"]
            return text, suggestions, cards

        # --- CAMPUS FACILITIES ---
        if intent == "campus_facilities":
            fac_info = self.knowledge_base.get_policy("campus_facilities")
            text = f"### 🏫 {fac_info['summary']}\n\n{fac_info['details']}"
            suggestions = ["Library hours", "Fee payment deadlines", "Exam schedule"]
            return text, suggestions, cards

        # --- ADMISSION & FEES ---
        if intent == "admission_fees":
            fee_info = self.knowledge_base.get_policy("admission_fees")
            text = f"### 💳 {fee_info['summary']}\n\n{fee_info['details']}"
            suggestions = ["Available scholarships", "Grading policy", "Hostel facilities"]
            return text, suggestions, cards

        # --- FALLBACK & INTELLIGENT KNOWLEDGE SEARCH ---
        search_res = self.knowledge_base.search_knowledge(raw_message)

        if search_res.type != "none" if hasattr(search_res, "type") else search_res.get("type") != "none":
            stype = search_res.get("type")

            # 1. Project Ideas Response
            if stype == "project_ideas":
                domain_name = search_res.get("domain", "Computer Science")
                ideas = search_res.get("ideas", [])
                formatted_ideas = []
                for idx, p in enumerate(ideas, 1):
                    formatted_ideas.append(
                        f"### {idx}. {p['title']} ({p['level']})\n"
                        f"• **Domain:** {p['domain']}\n"
                        f"• **Tech Stack:** `{p['tech']}`\n"
                        f"• **Overview:** {p['desc']}\n"
                        f"• **Key Highlights:** {p.get('features', '')}\n"
                    )
                text = (
                    f"Here are top recommended **{domain_name} project ideas** tailored for your academic portfolio:\n\n"
                    + "\n".join(formatted_ideas) +
                    "Which of these would you like to build or explore further?"
                )
                suggestions = ["Python project ideas", "Web dev project ideas", "AI ML project ideas", "DSA projects"]
                return text, suggestions, cards

            # 2. Technical Concept Response
            if stype == "technical_concept":
                c = search_res.get("concept", {})
                sections = [f"### 💡 {c['title']} ({c.get('category', 'Computer Science')})\n\n{c['summary']}"]
                if "operations" in c:
                    sections.append(f"**Key Operations & Time Complexity:**\n{c['operations']}")
                if "complexity" in c:
                    sections.append(f"**Complexity Analysis:**\n{c['complexity']}")
                if "how_it_works" in c:
                    sections.append(f"**Working Principle:**\n{c['how_it_works']}")
                if "types" in c:
                    sections.append(f"**Variations & Types:**\n{c['types']}")
                if "comparison" in c:
                    sections.append(f"**Key Differences:**\n{c['comparison']}")
                if "applications" in c:
                    sections.append(f"**Real-World Applications:**\n{c['applications']}")
                if "pros_cons" in c:
                    sections.append(f"**Trade-offs:**\n{c['pros_cons']}")
                text = "\n\n".join(sections)
                suggestions = ["Syllabus for CS201", "Python project idea", "Exam schedule", "Ask another concept"]
                return text, suggestions, cards

            # 3. Study & Career Guidance Response
            if stype == "study_guidance":
                g = search_res.get("guide", {})
                text = f"### 🎯 {g['title']}\n\n{g['content']}"
                suggestions = ["Placement roadmap", "Exam preparation tips", "How CGPA is calculated", "Course list"]
                return text, suggestions, cards

            # 4. Syllabus Module Match
            if stype == "syllabus_topics":
                match_bullets = []
                for item in search_res.get("topics", []):
                    for mod in item["modules"]:
                        match_bullets.append(f"• In **{item['course_code']} ({item['course_title']})**: {mod}")
                text = (
                    f"I searched our academic curriculum and found matching modules for your query:\n\n"
                    + "\n".join(match_bullets) +
                    "\n\nWould you like more details on any of these courses?"
                )
                suggestions = [f"Tell me about {search_res['topics'][0]['course_code']}", "View all courses", "Exam schedule"]
                return text, suggestions, cards

            # 5. Campus Policy Match
            if stype == "campus_policy":
                pol = search_res.get("policy", {})
                text = f"### ℹ️ {pol['summary']}\n\n{pol['details']}"
                suggestions = ["Exam schedule", "Grading policy", "Library services"]
                return text, suggestions, cards

        # Default fallback if nothing matches
        text = (
            "I'm here to assist you! You can ask me about:\n"
            "• **Project Ideas:** *'Give me python project ideas'*, *'Web dev project ideas'*\n"
            "• **Course Syllabi:** *'Syllabus for CS201'*, *'Tell me about CS101'*\n"
            "• **Technical Concepts:** *'What is a stack'*, *'Explain binary search'*, *'List vs tuple'*\n"
            "• **Campus Regulations:** *'When are exams?'*, *'How is CGPA calculated?'*, *'Library timings'*\n"
            "• **Placement & Careers:** *'Placement preparation roadmap'*, *'Study tips'*"
        )
        suggestions = ["Give me python project ideas", "List available courses", "When are the exams?", "How is CGPA calculated?"]
        return text, suggestions, cards
