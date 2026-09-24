"""
Unit tests for KnowledgeBase and DialogueManager.
"""
import pytest
from core.knowledge_base import KnowledgeBase
from core.dialogue_manager import DialogueManager


@pytest.fixture
def kb():
    return KnowledgeBase()


@pytest.fixture
def dm():
    return DialogueManager()


def test_get_course_by_code(kb):
    course = kb.get_course("CS101")
    assert course is not None
    assert "Python" in course["title"]
    assert course["credits"] == 4


def test_get_syllabus_contains_modules(kb):
    syllabus = kb.get_syllabus("CS201")
    assert syllabus is not None
    assert len(syllabus) >= 5
    assert any("Stacks" in mod for mod in syllabus)


def test_policy_lookup(kb):
    grading = kb.get_policy("grading_policy")
    assert grading is not None
    assert "75%" in grading["details"]


def test_dialogue_manager_session_persistence(dm):
    session_id = "test_user_session_1"
    res1 = dm.process_message(session_id, "Tell me about CS201 course")
    assert "CS201" in res1["response"]
    assert dm.sessions[session_id]["active_course"] == "CS201"

    # Follow-up without explicitly naming CS201
    res2 = dm.process_message(session_id, "What is the syllabus?")
    assert "CS201" in res2["response"]
    assert "Module" in res2["response"]
