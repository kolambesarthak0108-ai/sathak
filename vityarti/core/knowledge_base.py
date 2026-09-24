"""
Module: core.knowledge_base
Purpose: Structured college knowledge repository and semantic/keyword search engine.
"""
from typing import Dict, Any, List, Optional


COURSES_DATA: Dict[str, Dict[str, Any]] = {
    "CS101": {
        "title": "Introduction to Programming (Python)",
        "code": "CS101",
        "credits": 4,
        "instructor": "Dr. Sunil Patel (Cabin: Tech Block 204, Email: spatel@campus.edu)",
        "prerequisites": "None",
        "syllabus": [
            "Module 1: Python Fundamentals, Data Types, Control Structures, Loops",
            "Module 2: Functions, Recursion, Scope, and Lambda Expressions",
            "Module 3: Data Structures (Lists, Tuples, Dictionaries, Sets)",
            "Module 4: File I/O, Exception Handling, and Modular Programming",
            "Module 5: Object-Oriented Programming (Classes, Inheritance, Polymorphism)",
            "Module 6: Standard Libraries and Basic GUI Development"
        ],
        "schedule": "Monday & Wednesday: 10:00 AM - 11:30 AM (LH-1)",
        "exam_weightage": "CAT-1: 15%, CAT-2: 15%, Lab/Assignments: 30%, FAT: 40%"
    },
    "CS201": {
        "title": "Data Structures and Algorithms",
        "code": "CS201",
        "credits": 4,
        "instructor": "Dr. R. K. Sharma (Cabin: Tech Block 301, Email: rksharma@campus.edu)",
        "prerequisites": "CS101 - Programming in Python or C++",
        "syllabus": [
            "Module 1: Asymptotic Analysis (Big-O, Omega, Theta), Arrays, Strings",
            "Module 2: Singly, Doubly, and Circular Linked Lists",
            "Module 3: Stacks & Queues (Applications, Infix-to-Postfix conversion)",
            "Module 4: Trees, Binary Search Trees, AVL Trees, Heaps",
            "Module 5: Graphs (BFS, DFS, Dijkstra, Prim & Kruskal MST)",
            "Module 6: Sorting & Searching (Merge Sort, Quick Sort, Hash Tables)"
        ],
        "schedule": "Tuesday & Thursday: 09:00 AM - 10:30 AM (LH-3)",
        "exam_weightage": "CAT-1: 15%, CAT-2: 15%, Quizzes: 20%, FAT: 50%"
    },
    "CS301": {
        "title": "Artificial Intelligence & Machine Learning",
        "code": "CS301",
        "credits": 4,
        "instructor": "Prof. Ananya Verma (Cabin: AI Innovation Lab 102, Email: averma@campus.edu)",
        "prerequisites": "CS201 - Data Structures, MAT101 - Linear Algebra",
        "syllabus": [
            "Module 1: Introduction to AI, Intelligent Agents, State Space Search",
            "Module 2: Heuristic Search (A*, Greedy Best-First, Minimax with Alpha-Beta)",
            "Module 3: Supervised Learning (Linear/Logistic Regression, Decision Trees)",
            "Module 4: Unsupervised Learning (K-Means, PCA, Hierarchical Clustering)",
            "Module 5: Neural Networks, Perceptron, Backpropagation Basics",
            "Module 6: Natural Language Processing & Ethical AI considerations"
        ],
        "schedule": "Wednesday & Friday: 02:00 PM - 03:30 PM (LH-5)",
        "exam_weightage": "Continuous Assessment: 30%, Midterm: 20%, Project: 20%, Final: 30%"
    },
    "CS302": {
        "title": "Full Stack Web Development",
        "code": "CS302",
        "credits": 3,
        "instructor": "Dr. Sunil Patel (Cabin: Tech Block 204, Email: spatel@campus.edu)",
        "prerequisites": "CS101 - Basic Programming",
        "syllabus": [
            "Module 1: Semantic HTML5, Modern CSS3, Flexbox, Grid, Responsive Design",
            "Module 2: Modern JavaScript (ES6+), DOM Manipulation, Event Listeners",
            "Module 3: Frontend Frameworks & Single Page Architecture",
            "Module 4: Backend REST APIs with Python (Flask/FastAPI) and Node.js",
            "Module 5: Relational & Document Databases (SQLite, PostgreSQL, MongoDB)",
            "Module 6: Web Security (JWT, CORS, XSS, CSRF) & Cloud Deployment"
        ],
        "schedule": "Monday & Friday: 11:30 AM - 01:00 PM (Lab 4)",
        "exam_weightage": "Lab Exams: 40%, Mini-Project: 30%, Final Theory: 30%"
    },
    "MAT101": {
        "title": "Discrete Mathematics & Linear Algebra",
        "code": "MAT101",
        "credits": 4,
        "instructor": "Prof. Priya Gupta (Cabin: Science Block 112, Email: pgupta@campus.edu)",
        "prerequisites": "Standard 12th Mathematics",
        "syllabus": [
            "Module 1: Propositional & Predicate Logic, Proof Techniques",
            "Module 2: Set Theory, Relations, Equivalence, Partial Orderings",
            "Module 3: Combinatorics, Pigeonhole Principle, Recurrence Relations",
            "Module 4: Graph Theory (Euler, Hamilton, Trees, Planarity)",
            "Module 5: Matrix Algebra, Vector Spaces, Subspaces, Basis, Dimension",
            "Module 6: Eigenvalues, Eigenvectors, Diagonalization, Singular Value Decomp"
        ],
        "schedule": "Monday & Thursday: 08:00 AM - 09:30 AM (LH-2)",
        "exam_weightage": "CAT-1: 20%, CAT-2: 20%, Assignments: 10%, FAT: 50%"
    }
}


GENERAL_KNOWLEDGE: Dict[str, Dict[str, str]] = {
    "grading_policy": {
        "summary": "10-Point Relative / Absolute Grading System",
        "details": (
            "• S Grade: 90-100% (10 grade points - Outstanding)\n"
            "• A Grade: 80-89% (9 grade points - Excellent)\n"
            "• B Grade: 70-79% (8 grade points - Very Good)\n"
            "• C Grade: 60-69% (7 grade points - Good)\n"
            "• D Grade: 50-59% (6 grade points - Pass)\n"
            "• F Grade: Below 50% (0 grade points - Fail/Reappear)\n\n"
            "**Attendance Requirement:** A minimum of **75% aggregate attendance** is mandatory to appear for the Final Assessment Test (FAT). Students with 70-74% require medical approval."
        )
    },
    "exam_schedule": {
        "summary": "Current Academic Semester Examination Windows",
        "details": (
            "• **Continuous Assessment Test 1 (CAT-1):** October 12 – October 18\n"
            "• **Continuous Assessment Test 2 (CAT-2):** November 15 – November 21\n"
            "• **Lab Practical Examinations:** December 01 – December 07\n"
            "• **Final Assessment Test (FAT):** December 14 – December 28\n"
            "• **Hall Tickets:** Downloadable from the Student Portal 5 days before exams."
        )
    },
    "library_services": {
        "summary": "Central Campus Library Information",
        "details": (
            "• **Operating Hours:** Monday to Saturday: 8:00 AM - 10:00 PM | Sunday: 9:00 AM - 5:00 PM\n"
            "• **Borrowing Policy:** Undergraduates can borrow up to 4 books for 14 days with 1 renewal.\n"
            "• **Digital Library:** Accessible 24/7 via campus portal or VPN (IEEE, ACM, Springer, JSTOR).\n"
            "• **Facilities:** Quiet reading hall (Level 2), Discussion cubicles (Level 3), Printing kiosk (Ground Floor)."
        )
    },
    "campus_facilities": {
        "summary": "Campus Amenities & Important Contacts",
        "details": (
            "• **Hostel Curfew:** 09:00 PM on weekdays, 09:30 PM on weekends.\n"
            "• **Dining / Mess Timings:** Breakfast (07:30-09:00), Lunch (12:00-14:00), Dinner (19:30-21:30).\n"
            "• **Health Center:** 24/7 emergency care located near Hostel Block A. Call ext: 108.\n"
            "• **Campus Wi-Fi:** SSID: 'Campus-Secure' (Login using Student Registration ID & NetID password).\n"
            "• **Transport / Shuttle:** Electric shuttle runs every 15 minutes between North and South Gates."
        )
    },
    "admission_fees": {
        "summary": "Tuition Fees & Scholarship Details",
        "details": (
            "• **Tuition Payment Window:** Open from 1st to 20th of every semester start.\n"
            "• **Online Portal:** Pay via NetBanking, UPI, or Credit Card on student ERP portal.\n"
            "• **Late Fee:** Rs. 500 per week after the deadline.\n"
            "• **Merit Scholarships:** 50% tuition waiver for top 2% semester rank holders; sports/economic aid available via Student Welfare Office."
        )
    }
}


PROJECT_IDEAS: Dict[str, List[Dict[str, Any]]] = {
    "python": [
        {
            "title": "Campus AI Academic & College Chatbot",
            "domain": "Python / NLP / Web",
            "level": "Intermediate",
            "tech": "Python, Flask, TF-IDF / NLTK, SQLite, HTML5/CSS3, Web Speech API",
            "desc": "An intelligent conversational assistant for university students that answers syllabus inquiries, faculty contacts, and grading policies using NLP text processing and voice speech interfaces.",
            "features": "Intent classification, TF-IDF vectorization, speech recognition (STT/TTS), SQLite session analytics."
        },
        {
            "title": "Smart Attendance System via OpenCV & Face Recognition",
            "domain": "Python / Computer Vision",
            "level": "Intermediate",
            "tech": "Python, OpenCV, face_recognition, dlib, SQLite / CSV",
            "desc": "Automates student classroom attendance by detecting and recognizing student faces from a webcam video stream in real-time, logging entry timestamps automatically.",
            "features": "Real-time face detection, embedding matching, attendance CSV export, proxy attendance prevention."
        },
        {
            "title": "Automated Resume Screener & Skill Matcher",
            "domain": "Python / NLP / Machine Learning",
            "level": "Intermediate to Advanced",
            "tech": "Python, PyPDF2, spaCy / NLTK, Scikit-learn, Streamlit",
            "desc": "Parses student resumes in PDF format, extracts key skills, education, and experience, and ranks applicants against job descriptions using Cosine Similarity.",
            "features": "PDF text extraction, entity recognition for technical skills, TF-IDF similarity score, interactive web dashboard."
        },
        {
            "title": "Source Code Plagiarism & Syntax Tree Analyzer",
            "domain": "Python / Software Engineering",
            "level": "Advanced",
            "tech": "Python, ast module, difflib, NetworkX, Flask",
            "desc": "Analyzes programming assignment submissions for structural plagiarism by comparing Abstract Syntax Trees (AST) rather than simple text string matching.",
            "features": "AST parsing, variable renaming tolerance, structural graph similarity, visual side-by-side diff."
        },
        {
            "title": "Weather & Environmental Air Quality Forecaster",
            "domain": "Python / Data Science / APIs",
            "level": "Beginner to Intermediate",
            "tech": "Python, Requests, OpenWeather API, Pandas, Matplotlib / Plotly",
            "desc": "Fetches live meteorological and AQI data, analyzes historical trends, and predicts weather conditions using time-series forecasting.",
            "features": "Live REST API consumption, historical data visualization, predictive rainfall indicators."
        }
    ],
    "web": [
        {
            "title": "Peer-to-Peer Campus Marketplace & Book Exchange",
            "domain": "Web Development / Full Stack",
            "level": "Intermediate",
            "tech": "HTML5, Vanilla CSS / Tailwind, JavaScript, Flask / Node.js, SQLite",
            "desc": "A dedicated campus platform for students to buy, sell, or rent textbooks, lab equipment, notes, and hostel essentials within their college community.",
            "features": "User authentication, listing creation with image uploads, internal student chat, search & filter."
        },
        {
            "title": "Online Code Compiler & Evaluation Sandbox",
            "domain": "Web Development / DevOps",
            "level": "Advanced",
            "tech": "JavaScript, Monaco Editor, Python (Flask), Docker, WebSockets",
            "desc": "A browser-based code runner supporting Python, C++, and Java that executes user code in isolated Docker sandbox containers against test cases.",
            "features": "Syntax highlighting, sandboxed execution, memory and CPU limits, automated test case judging."
        },
        {
            "title": "Student Portfolio & Academic Project Showcase",
            "domain": "Web Development / Frontend",
            "level": "Beginner to Intermediate",
            "tech": "HTML5, Modern CSS (Glassmorphism), Vanilla JavaScript",
            "desc": "A dynamic portfolio website allowing students to highlight projects, certifications, GitHub contributions, and research papers with interactive dark mode and contact forms.",
            "features": "Dynamic project cards, interactive modals, responsive glassmorphic UI, contact email integration."
        }
    ],
    "ai_ml": [
        {
            "title": "Disease Prediction System using Clinical Parameters",
            "domain": "Machine Learning / Healthcare",
            "level": "Intermediate",
            "tech": "Python, Scikit-learn, XGBoost, Pandas, Streamlit / Flask",
            "desc": "Predicts the likelihood of chronic ailments (e.g., Diabetes, Cardio, Kidney disease) using patient clinical test metrics with high accuracy.",
            "features": "Data preprocessing & imputation, feature importance graphs, multi-model comparison, confidence metrics."
        },
        {
            "title": "Real-Time Sign Language Gesture Recognition",
            "domain": "Deep Learning / Computer Vision",
            "level": "Advanced",
            "tech": "Python, MediaPipe, OpenCV, TensorFlow / Keras, NumPy",
            "desc": "Translates hand sign gestures captured from camera into text and audible speech in real time to assist hearing and speech-impaired individuals.",
            "features": "21-hand landmark extraction, LSTM / CNN gesture classification, real-time audio playback."
        },
        {
            "title": "Stock Market Trend Prediction with LSTM Networks",
            "domain": "Deep Learning / Finance",
            "level": "Advanced",
            "tech": "Python, yfinance, PyTorch / TensorFlow, Pandas, Plotly",
            "desc": "Trains Long Short-Term Memory (LSTM) recurrent neural networks on historical stock time series data to forecast future price movements and technical indicators.",
            "features": "Live Yahoo Finance streaming, moving average overlays, train/test error evaluation."
        }
    ],
    "dsa": [
        {
            "title": "Interactive Graph Algorithms & Pathfinding Visualizer",
            "domain": "Data Structures & Algorithms",
            "level": "Intermediate",
            "tech": "JavaScript (ES6+), HTML5 Canvas / DOM, CSS3",
            "desc": "Visualizes classic graph algorithms in real-time on a 2D grid: Dijkstra's Algorithm, A* Search, Breadth-First Search (BFS), and Depth-First Search (DFS).",
            "features": "Wall creation, weighted nodes, speed controls, step-by-step path exploration animation."
        },
        {
            "title": "Huffman Coding File Compression Utility",
            "domain": "Algorithms / Systems",
            "level": "Intermediate",
            "tech": "Python or C++, Binary File I/O, Heap / Priority Queue",
            "desc": "Lossless text file compressor using Huffman Coding prefix trees, reducing file sizes by 30-50% while preserving original data intact.",
            "features": "Frequency table generation, Huffman tree building, bitwise file encoding & decoding."
        }
    ]
}


TECHNICAL_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "stack": {
        "title": "Stack Data Structure",
        "category": "Data Structures",
        "summary": "A linear data structure following the **LIFO (Last In, First Out)** principle.",
        "operations": "• `push(x)`: Insert element on top (O(1))\n• `pop()`: Remove and return top element (O(1))\n• `peek()` / `top()`: Inspect top element without removing (O(1))\n• `isEmpty()`: Check if stack has elements (O(1))",
        "applications": "Function call stack, undo/redo mechanisms in text editors, parentheses matching, expression evaluation (Infix to Postfix)."
    },
    "queue": {
        "title": "Queue Data Structure",
        "category": "Data Structures",
        "summary": "A linear data structure adhering to the **FIFO (First In, First Out)** principle.",
        "operations": "• `enqueue(x)`: Add element to rear (O(1))\n• `dequeue()`: Remove element from front (O(1))\n• `front()`: View the first element (O(1))",
        "applications": "CPU task scheduling, Breadth-First Search (BFS) graph traversal, printer job spooling, message queues (Kafka/RabbitMQ)."
    },
    "binary search": {
        "title": "Binary Search Algorithm",
        "category": "Algorithms",
        "summary": "An efficient divide-and-conquer algorithm to find the position of a target value within a **sorted array**.",
        "complexity": "• **Time Complexity:** O(log n) worst and average case, O(1) best case\n• **Space Complexity:** O(1) iterative, O(log n) recursive call stack",
        "how_it_works": "1. Compare target with middle element.\n2. If equal, target is found.\n3. If target is smaller, search the left half.\n4. If target is larger, search the right half.\n5. Repeat until found or search space is exhausted."
    },
    "linked list": {
        "title": "Linked List Data Structure",
        "category": "Data Structures",
        "summary": "A linear collection of data elements called **nodes**, where each node contains data and a pointer (or reference) to the next node.",
        "types": "• **Singly Linked List:** Forward pointer only\n• **Doubly Linked List:** Both forward (`next`) and backward (`prev`) pointers\n• **Circular Linked List:** Last node links back to the head node",
        "pros_cons": "• **Advantage:** Dynamic size, O(1) insertions/deletions once pointer is known.\n• **Disadvantage:** O(n) linear search, no random index access, extra memory for pointer storage."
    },
    "binary search tree": {
        "title": "Binary Search Tree (BST)",
        "category": "Data Structures",
        "summary": "A node-based binary tree with the BST invariant: all keys in the left subtree are less than the node's key, and all keys in the right subtree are greater.",
        "complexity": "• Average Search/Insert/Delete: O(log n)\n• Worst case (degenerate/skewed tree): O(n)\n• Balanced variants (AVL, Red-Black Trees) guarantee O(log n) worst-case time."
    },
    "recursion": {
        "title": "Recursion in Computer Science",
        "category": "Programming Concepts",
        "summary": "A method of solving a problem where a function calls itself to solve smaller instances of the same problem.",
        "key_parts": "1. **Base Case:** The stopping condition that prevents infinite execution and stack overflow.\n2. **Recursive Step:** The logic that reduces the problem towards the base case.",
        "examples": "Factorial, Fibonacci sequence, Tree traversals (Inorder, Preorder, Postorder), Divide & Conquer (Merge Sort, Quick Sort)."
    },
    "python list vs tuple": {
        "title": "Python: List vs Tuple",
        "category": "Python Programming",
        "summary": "Key distinctions between Python's primary sequence types:",
        "comparison": "• **Mutability:** Lists are *mutable* (elements can be added, changed, or deleted); Tuples are *immutable*.\n• **Syntax:** Lists use square brackets `[1, 2]`; Tuples use parentheses `(1, 2)`.\n• **Performance:** Tuples are faster and use less memory due to static memory allocation.\n• **Dictionary Keys:** Tuples can be used as dictionary keys (if containing hashable elements); Lists cannot."
    },
    "machine learning": {
        "title": "Machine Learning Fundamentals",
        "category": "AI / ML",
        "summary": "A subset of Artificial Intelligence where computer systems learn patterns from historical data to make predictions or decisions without being explicitly programmed.",
        "types": "• **Supervised Learning:** Trained on labeled data (Regression, Classification - e.g., Linear Regression, Random Forest).\n• **Unsupervised Learning:** Discovers hidden structures in unlabeled data (Clustering, PCA - e.g., K-Means).\n• **Reinforcement Learning:** Agents learn optimal policies through trial, error, and reward signals (e.g., Q-Learning)."
    },
    "rest api": {
        "title": "RESTful API Architecture",
        "category": "Web Development",
        "summary": "Representational State Transfer (REST) is a software architectural style for building scalable web services over HTTP.",
        "principles": "• **Statelessness:** Each request from client to server must contain all information needed to process it.\n• **Standard HTTP Methods:** `GET` (retrieve), `POST` (create), `PUT`/`PATCH` (update), `DELETE` (remove).\n• **Standard Formats:** Data typically transferred as lightweight JSON payloads."
    }
}


STUDY_GUIDANCE: Dict[str, Dict[str, str]] = {
    "exam_tips": {
        "title": "Proven Academic Exam Preparation Strategies",
        "content": (
            "1. **Continuous Assessment Focus (CAT-1 & CAT-2):** Internal tests account for 30-40% of your total grade. Scoring high in CATs reduces pressure during Final Assessment Tests (FAT).\n"
            "2. **Active Recall & Spaced Repetition:** Instead of passive re-reading, test yourself with past exam papers and practice questions.\n"
            "3. **Module Weightage Prioritization:** Focus on foundational modules (Modules 1-3) early, as later modules build directly upon them.\n"
            "4. **Attendance Safety Margin:** Keep attendance comfortably above 80% to avoid debarment or emergency medical condonations."
        )
    },
    "placement_roadmap": {
        "title": "Campus Placement & Internship Roadmap",
        "content": (
            "1. **Data Structures & Algorithms (DSA):** Master Arrays, Linked Lists, Stacks, Queues, Trees, Graphs, and Dynamic Programming. Practice on LeetCode / HackerRank (target 100-150 problems).\n"
            "2. **Core CS Subjects:** Be ready to answer questions on Operating Systems (Processes, Threads, Deadlocks), DBMS (SQL queries, Normalization, ACID), and Computer Networks (OSI model, TCP/IP).\n"
            "3. **Capstone Projects:** Build at least 2 polished full-stack or AI/ML projects with GitHub repositories, documentation, and live demo links.\n"
            "4. **Aptitude & Soft Skills:** Practice quantitative aptitude, logical reasoning, and prepare structured answers using the STAR method (Situation, Task, Action, Result)."
        )
    },
    "cgpa_improvement": {
        "title": "Effective Strategies to Boost Your CGPA",
        "content": (
            "1. **Never Skip Lab Practical Exams or Quizzes:** Laboratory assignments and digital assignments represent easy, high-percentage marks that directly boost your internal score.\n"
            "2. **Target High-Credit Courses First:** A 4-credit course affects your GPA twice as much as a 2-credit course.\n"
            "3. **Attend Office Hours:** Clarify doubts with course faculty during designated cabin hours early in the semester rather than right before exams."
        )
    }
}


class KnowledgeBase:
    """Manages queries into courses, faculty, exams, general policies, project ideas, and CS concepts."""

    def __init__(self):
        self.courses = COURSES_DATA
        self.general_kb = GENERAL_KNOWLEDGE
        self.project_ideas = PROJECT_IDEAS
        self.technical_concepts = TECHNICAL_CONCEPTS
        self.study_guidance = STUDY_GUIDANCE

    def get_all_courses(self) -> List[Dict[str, Any]]:
        """Return list of all registered course summaries."""
        return [
            {
                "code": c["code"],
                "title": c["title"],
                "credits": c["credits"],
                "instructor": c["instructor"].split("(")[0].strip()
            }
            for c in self.courses.values()
        ]

    def get_course(self, course_key: str) -> Optional[Dict[str, Any]]:
        """Look up course by code (e.g. CS101) or matching title keyword."""
        key = course_key.upper().replace(" ", "")
        if key in self.courses:
            return self.courses[key]
        for code, info in self.courses.items():
            if key in code or key in info["title"].upper():
                return info
        return None

    def get_syllabus(self, course_key: str) -> Optional[List[str]]:
        """Return syllabus modules for a course."""
        course = self.get_course(course_key)
        return course["syllabus"] if course else None

    def get_policy(self, topic_key: str) -> Optional[Dict[str, str]]:
        """Retrieve policy details for exam, grading, library, facilities, or fees."""
        return self.general_kb.get(topic_key)

    def get_project_ideas(self, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve curated project ideas filtered optionally by domain."""
        if domain and domain.lower() in self.project_ideas:
            return self.project_ideas[domain.lower()]
        
        # Default: return a curated cross-domain selection
        all_ideas = []
        for dom, ideas in self.project_ideas.items():
            all_ideas.extend(ideas)
        return all_ideas

    def search_topics(self, query: str) -> List[Dict[str, Any]]:
        """Search across courses for topics matching words in the query."""
        results = []
        words = [w for w in query.lower().split() if len(w) > 2 and w not in {"the", "and", "for", "with", "what", "how", "give", "tell"}]
        if not words:
            words = [query.lower()]
            
        for code, info in self.courses.items():
            matching_modules = []
            for mod in info["syllabus"]:
                mod_lower = mod.lower()
                if any(word in mod_lower for word in words):
                    matching_modules.append(mod)
            if matching_modules:
                results.append({
                    "course_code": code,
                    "course_title": info["title"],
                    "modules": matching_modules
                })
        return results

    def search_knowledge(self, query: str) -> Dict[str, Any]:
        """
        Universal intelligent knowledge search across:
        - Project Ideas (Python, Web, AI/ML, DSA)
        - Technical Concepts & Algorithms
        - Study & Career Guidance
        - Course Syllabi & Faculty
        - Campus Policies
        """
        q = query.lower()
        words = set([w for w in q.replace("?", "").replace("!", "").replace(",", "").split() if len(w) > 2])

        # 1. Project Ideas Search
        if any(term in q for term in ["project", "idea", "mini project", "final year", "capstone", "build"]):
            domain = None
            if "python" in q:
                domain = "python"
            elif any(t in q for t in ["web", "frontend", "full stack", "html", "javascript"]):
                domain = "web"
            elif any(t in q for t in ["ai", "ml", "machine learning", "deep learning", "neural"]):
                domain = "ai_ml"
            elif any(t in q for t in ["dsa", "data structure", "algorithm", "graph", "tree"]):
                domain = "dsa"

            ideas = self.get_project_ideas(domain)
            return {
                "type": "project_ideas",
                "domain": domain or "General / Computer Science",
                "ideas": ideas[:4]
            }

        # 2. Technical Concepts Search
        for concept_key, concept_data in self.technical_concepts.items():
            if concept_key in q or any(w in concept_key for w in words if len(w) > 3):
                return {
                    "type": "technical_concept",
                    "concept": concept_data
                }

        # 3. Study & Placement Guidance Search
        if any(term in q for term in ["placement", "interview", "job", "career", "internship", "hiring"]):
            return {
                "type": "study_guidance",
                "guide": self.study_guidance["placement_roadmap"]
            }
        if any(term in q for term in ["cgpa", "gpa", "marks", "improve grade", "score high"]):
            return {
                "type": "study_guidance",
                "guide": self.study_guidance["cgpa_improvement"]
            }
        if any(term in q for term in ["study tip", "how to study", "exam tip", "prepare for exam", "study strategy"]):
            return {
                "type": "study_guidance",
                "guide": self.study_guidance["exam_tips"]
            }

        # 4. Course syllabus topic search
        matched_topics = self.search_topics(q)
        if matched_topics:
            return {
                "type": "syllabus_topics",
                "topics": matched_topics
            }

        # 5. General Campus Policies
        for policy_key, policy_data in self.general_kb.items():
            if any(term in q for term in policy_key.split("_")):
                return {
                    "type": "campus_policy",
                    "policy": policy_data
                }

        return {"type": "none"}

