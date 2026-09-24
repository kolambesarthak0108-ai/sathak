"""
Unit tests for NLP text preprocessing module.
"""
import pytest
from nlp.preprocessor import TextPreprocessor


@pytest.fixture
def preprocessor():
    return TextPreprocessor()


def test_clean_sanitizes_urls_and_punctuation(preprocessor):
    raw = "Check out https://vit.ac.in for CS101! It's awesome???"
    cleaned = preprocessor.clean(raw)
    assert "https" not in cleaned
    assert "?" not in cleaned
    assert "cs101" in cleaned


def test_tokenize_filters_stopwords_preserves_intent_words(preprocessor):
    raw = "What is the syllabus for CS201 course?"
    tokens = preprocessor.tokenize(raw)
    # "what" is preserved as an intent-critical question word
    assert "what" in tokens
    assert "syllabus" in tokens
    assert "cs201" in tokens
    # "the" and "for" should be filtered out
    assert "the" not in tokens
    assert "for" not in tokens


def test_ngrams_generation(preprocessor):
    tokens = ["data", "structures", "algorithms"]
    bigrams = preprocessor.get_ngrams(tokens, 2)
    assert bigrams == ["data structures", "structures algorithms"]


def test_empty_string_handling(preprocessor):
    assert preprocessor.clean("") == ""
    assert preprocessor.tokenize("") == []
