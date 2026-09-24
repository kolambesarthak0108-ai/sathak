"""
Module: nlp.preprocessor
Purpose: Tokenization, text normalization, stopword filtering, and n-gram extraction.
"""
import re
from typing import List, Set

# Common English stopwords suitable for academic chatbot queries
STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
    "during", "each", "few", "for", "from", "further", "had", "hadn't", "has",
    "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her",
    "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's",
    "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
    "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
    "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't",
    "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
    "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
    "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
    "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

# Words with high intent value in questions that shouldn't be stripped in key contexts
INTENT_PRESERVED_WORDS = {"what", "when", "where", "who", "why", "how", "can", "is", "are"}


class TextPreprocessor:
    """Preprocesses and normalizes raw text for the NLP pipeline."""

    def __init__(self, remove_stopwords: bool = True):
        self.remove_stopwords = remove_stopwords

    def clean(self, text: str) -> str:
        """Sanitize text: remove URLs, special characters, and normalize spaces."""
        if not text:
            return ""
        # Lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r"https?://\S+|www\.\S+", "", text)
        # Remove special characters except alphanumerics, hyphens, and whitespace
        text = re.sub(r"[^\w\s\-]", " ", text)
        # Normalize multiple spaces
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text: str) -> List[str]:
        """Convert input text to cleaned list of tokens."""
        cleaned = self.clean(text)
        if not cleaned:
            return []
        tokens = cleaned.split()
        if self.remove_stopwords:
            # Preserve intent-critical words if the token set is small
            tokens = [t for t in tokens if t not in STOPWORDS or t in INTENT_PRESERVED_WORDS]
        return tokens

    def get_ngrams(self, tokens: List[str], n: int = 2) -> List[str]:
        """Generate n-grams from token sequence."""
        if len(tokens) < n:
            return []
        return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

    def extract_keywords(self, text: str, top_k: int = 5) -> List[str]:
        """Extract top keywords based on term frequency."""
        tokens = self.tokenize(text)
        freq = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        sorted_tokens = sorted(freq.items(), key=lambda item: item[1], reverse=True)
        return [word for word, count in sorted_tokens[:top_k]]
