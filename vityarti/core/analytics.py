"""
Module: core.analytics
Purpose: Real-time analytics, response time latency metrics, and user feedback tracking.
"""
import time
from typing import Dict, Any, List


class AnalyticsTracker:
    """Tracks runtime performance, intent distributions, and feedback metrics."""

    def __init__(self):
        self.total_queries: int = 0
        self.intent_counts: Dict[str, int] = {}
        self.latency_records: List[float] = []
        self.positive_feedback: int = 0
        self.negative_feedback: int = 0
        self.start_time: float = time.time()

    def record_query(self, intent: str, latency_ms: float) -> None:
        """Record an incoming interaction event."""
        self.total_queries += 1
        self.intent_counts[intent] = self.intent_counts.get(intent, 0) + 1
        self.latency_records.append(latency_ms)
        # Keep last 500 latency samples
        if len(self.latency_records) > 500:
            self.latency_records.pop(0)

    def record_feedback(self, rating: str) -> None:
        """Record user thumbs-up / thumbs-down."""
        if rating in ("positive", "like", "up"):
            self.positive_feedback += 1
        elif rating in ("negative", "dislike", "down"):
            self.negative_feedback += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Compute aggregated performance metrics."""
        avg_latency = (
            sum(self.latency_records) / len(self.latency_records)
            if self.latency_records
            else 0.0
        )
        total_feedback = self.positive_feedback + self.negative_feedback
        satisfaction_rate = (
            (self.positive_feedback / total_feedback) * 100
            if total_feedback > 0
            else 100.0
        )
        uptime_seconds = int(time.time() - self.start_time)

        return {
            "total_queries": self.total_queries,
            "average_latency_ms": round(avg_latency, 2),
            "intent_distribution": self.intent_counts,
            "satisfaction_rate": round(satisfaction_rate, 1),
            "positive_feedback": self.positive_feedback,
            "negative_feedback": self.negative_feedback,
            "uptime_seconds": uptime_seconds
        }
