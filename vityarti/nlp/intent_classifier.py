"""
Module: nlp.intent_classifier
Purpose: Intent classification using TF-IDF vectorization and Cosine Similarity scoring.
"""
import math
from typing import Dict, List, Tuple, Optional
from .preprocessor import TextPreprocessor


# Training data with representative utterances per intent
DEFAULT_INTENT_TRAINING_DATA: Dict[str, List[str]] = {
    "greeting": [
        "hello", "hi", "hey there", "good morning", "good evening", "hey bot",
        "greetings", "hello assistant", "hi there", "namaste"
    ],
    "goodbye": [
        "bye", "goodbye", "see you later", "catch you later", "exit", "quit",
        "have a good day", "bye bye", "talk to you soon"
    ],
    "bot_identity": [
        "who are you", "what is your name", "what can you do", "introduce yourself",
        "how can you help me", "what are your capabilities", "tell me about yourself",
        "are you an ai", "what is campusmind"
    ],
    "course_info": [
        "what courses are offered", "tell me about computer science program",
        "available subjects this semester", "course catalog", "elective options",
        "what subjects do i study", "list of courses", "data structures course",
        "python programming course", "ai and ml course"
    ],
    "syllabus_inquiry": [
        "what is the syllabus", "course content and topics", "what will be taught",
        "syllabus for data structures", "show course modules", "curriculum details",
        "units in ai course", "topics covered in web development"
    ],
    "exam_schedule": [
        "when are the exams", "exam timetable", "midterm dates", "final exam schedule",
        "when is the next test", "assessment calendar", "end semester exams",
        "hall ticket release date"
    ],
    "grading_policy": [
        "how is cgpa calculated", "grading system and policy", "minimum pass marks",
        "what is the attendance criteria", "minimum 75 percent attendance",
        "how does gpa grading work", "credits required for degree", "re-evaluation process"
    ],
    "faculty_contact": [
        "how to contact faculty", "professor email address", "hod contact details",
        "instructor office hours", "where is professor cabin", "faculty directory",
        "who is teaching cs201", "course instructor name"
    ],
    "library_services": [
        "what are library timings", "how to borrow books", "digital library access",
        "online journals and papers", "library fine rules", "central library location",
        "where can i study quietly", "renew borrowed book"
    ],
    "campus_facilities": [
        "hostel rules and curfew", "mess food and timings", "campus wifi setup",
        "sports complex and gym", "medical center and clinic", "bus and shuttle route",
        "canteen facilities", "lost and found office"
    ],
    "admission_fees": [
        "fee payment deadline", "how to pay college tuition", "scholarships available",
        "financial aid", "fee structure for btech", "payment gateway and receipt",
        "late fee fine details"
    ],
    "appreciation": [
        "thank you", "thanks a lot", "this was very helpful", "great job",
        "awesome response", "you are very smart", "thanks for the help"
    ]
}


class IntentClassifier:
    """Classifies user natural language input into predefined intent categories."""

    def __init__(self, confidence_threshold: float = 0.22):
        self.preprocessor = TextPreprocessor()
        self.confidence_threshold = confidence_threshold
        self.intent_training_data: Dict[str, List[str]] = {}
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.intent_vectors: Dict[str, List[float]] = {}
        self.train(DEFAULT_INTENT_TRAINING_DATA)

    def train(self, data: Dict[str, List[str]]) -> None:
        """Build TF-IDF vocabulary and centroid vectors for each intent."""
        self.intent_training_data = data
        all_documents: List[str] = []
        intent_doc_map: Dict[str, List[str]] = {}

        for intent, utterances in data.items():
            intent_doc_map[intent] = utterances
            all_documents.extend(utterances)

        # 1. Build vocabulary
        vocab_set = set()
        tokenized_docs = []
        for doc in all_documents:
            tokens = self.preprocessor.tokenize(doc)
            tokenized_docs.append(tokens)
            vocab_set.update(tokens)

        self.vocabulary = {term: idx for idx, term in enumerate(sorted(vocab_set))}
        n_docs = len(all_documents)

        # 2. Compute Inverse Document Frequency (IDF)
        self.idf = {}
        for term in self.vocabulary:
            doc_freq = sum(1 for tokens in tokenized_docs if term in tokens)
            # Smooth IDF
            self.idf[term] = math.log((1 + n_docs) / (1 + doc_freq)) + 1.0

        # 3. Compute centroid TF-IDF vector for each intent
        self.intent_vectors = {}
        for intent, utterances in intent_doc_map.items():
            aggregated_vector = [0.0] * len(self.vocabulary)
            for utt in utterances:
                utt_vec = self._vectorize(utt)
                for i in range(len(aggregated_vector)):
                    aggregated_vector[i] += utt_vec[i]
            
            # Normalize centroid
            norm = math.sqrt(sum(v * v for v in aggregated_vector))
            if norm > 0:
                self.intent_vectors[intent] = [v / norm for v in aggregated_vector]
            else:
                self.intent_vectors[intent] = aggregated_vector

    def _vectorize(self, text: str) -> List[float]:
        """Convert single text into normalized TF-IDF vector."""
        tokens = self.preprocessor.tokenize(text)
        vec = [0.0] * len(self.vocabulary)
        if not tokens:
            return vec

        tf = {}
        for token in tokens:
            if token in self.vocabulary:
                tf[token] = tf.get(token, 0) + 1

        for token, count in tf.items():
            idx = self.vocabulary[token]
            tf_weight = count / len(tokens)
            vec[idx] = tf_weight * self.idf[token]

        # L2 Normalize
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Compute cosine similarity between two unit vectors."""
        return sum(a * b for a, b in zip(vec_a, vec_b))

    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict the most likely intent and associated confidence score.
        Returns: (intent_name, confidence_score)
        """
        user_vec = self._vectorize(text)
        
        # If no words matched vocabulary, fallback
        if all(v == 0.0 for v in user_vec):
            # Check for direct keyword matches
            cleaned = self.preprocessor.clean(text)
            if any(k in cleaned for k in ["hi", "hello", "hey"]):
                return "greeting", 0.85
            if any(k in cleaned for k in ["bye", "see you"]):
                return "goodbye", 0.85
            if any(k in cleaned for k in ["who are you", "what can you do"]):
                return "bot_identity", 0.85
            return "fallback", 0.0

        best_intent = "fallback"
        best_score = 0.0

        for intent, centroid_vec in self.intent_vectors.items():
            sim = self._cosine_similarity(user_vec, centroid_vec)
            if sim > best_score:
                best_score = sim
                best_intent = intent

        if best_score < self.confidence_threshold:
            return "fallback", round(best_score, 3)

        return best_intent, round(best_score, 3)

    def get_ranked_intents(self, text: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Return top_k predictions with confidence scores."""
        user_vec = self._vectorize(text)
        scores = []
        for intent, centroid_vec in self.intent_vectors.items():
            sim = self._cosine_similarity(user_vec, centroid_vec)
            scores.append((intent, round(sim, 3)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
