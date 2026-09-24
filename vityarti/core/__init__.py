"""
Core Package for CampusMind AI Chatbot
Contains knowledge repository, dialogue management, and analytics tracking.
"""
from .knowledge_base import KnowledgeBase
from .dialogue_manager import DialogueManager
from .analytics import AnalyticsTracker

__all__ = ["KnowledgeBase", "DialogueManager", "AnalyticsTracker"]
