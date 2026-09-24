"""
Unit tests for intent classification and confidence scoring.
"""
import pytest
from nlp.intent_classifier import IntentClassifier
from nlp.entity_extractor import EntityExtractor


@pytest.fixture
def classifier():
    return IntentClassifier()


@pytest.fixture
def extractor():
    return EntityExtractor()


def test_greeting_intent_classification(classifier):
    intent, score = classifier.predict("Hello there, good morning!")
    assert intent == "greeting"
    assert score > 0.3


def test_exam_schedule_intent_classification(classifier):
    intent, score = classifier.predict("When are the midterm exams and final test?")
    assert intent == "exam_schedule"
    assert score > 0.3


def test_syllabus_inquiry_intent(classifier):
    intent, score = classifier.predict("What is the syllabus and topics covered?")
    assert intent == "syllabus_inquiry"
    assert score > 0.3


def test_grading_policy_intent(classifier):
    intent, score = classifier.predict("How is CGPA calculated and what is passing marks?")
    assert intent == "grading_policy"
    assert score > 0.3


def test_unrecognized_query_fallback(classifier):
    # Completely out of domain query
    intent, score = classifier.predict("quantum teleportation in outer space aliens")
    assert intent == "fallback"


def test_entity_extractor_detects_course_code(extractor):
    entities = extractor.extract("What are the prerequisites for CS201 course?")
    assert entities.get("course_code") == "CS201"


def test_entity_extractor_detects_course_alias(extractor):
    entities = extractor.extract("Show me the syllabus for Data Structures")
    assert entities.get("course_code") == "CS201"
