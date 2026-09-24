"""
Module: models.database
Purpose: SQLite database interface for persisting chat sessions, interactions, and user feedback.
"""
import sqlite3
import os
import time
from typing import Dict, Any, List, Optional


# Use /tmp on Vercel/serverless environments because root filesystem is read-only
if os.environ.get("VERCEL"):
    DEFAULT_DB_PATH = "/tmp/campusmind.db"
else:
    DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "campusmind.db")


class DatabaseManager:
    """Manages SQLite schema creation and CRUD operations for chat persistence."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Create and return a database connection with dictionary row access."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Create necessary tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Sessions Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at REAL NOT NULL,
                    last_active REAL NOT NULL,
                    metadata TEXT
                )
            """)

            # Chat Logs Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    intent TEXT,
                    confidence REAL,
                    latency_ms REAL,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)

            # User Feedback Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    rating TEXT NOT NULL,
                    comment TEXT,
                    timestamp REAL NOT NULL
                )
            """)
            conn.commit()

    def register_session(self, session_id: str, metadata: str = "") -> None:
        """Record or update active session timestamp."""
        now = time.time()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sessions (session_id, created_at, last_active, metadata)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET last_active = excluded.last_active
            """, (session_id, now, now, metadata))
            conn.commit()

    def log_interaction(
        self,
        session_id: str,
        user_message: str,
        bot_response: str,
        intent: str,
        confidence: float,
        latency_ms: float
    ) -> int:
        """Store conversational interaction record."""
        now = time.time()
        self.register_session(session_id)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chat_logs (session_id, timestamp, user_message, bot_response, intent, confidence, latency_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (session_id, now, user_message, bot_response, intent, confidence, latency_ms))
            conn.commit()
            return cursor.lastrowid

    def save_feedback(self, session_id: str, rating: str, comment: Optional[str] = None) -> int:
        """Persist user feedback."""
        now = time.time()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback (session_id, rating, comment, timestamp)
                VALUES (?, ?, ?, ?)
            """, (session_id, rating, comment or "", now))
            conn.commit()
            return cursor.lastrowid

    def get_session_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent interaction history for a given session."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, timestamp, user_message, bot_response, intent, confidence, latency_ms
                FROM chat_logs
                WHERE session_id = ?
                ORDER BY timestamp ASC
                LIMIT ?
            """, (session_id, limit))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_summary_stats(self) -> Dict[str, Any]:
        """Aggregate stored statistics from the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM chat_logs")
            total_messages = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT session_id) FROM sessions")
            total_sessions = cursor.fetchone()[0]

            cursor.execute("SELECT AVG(latency_ms) FROM chat_logs")
            avg_latency = cursor.fetchone()[0] or 0.0

            cursor.execute("SELECT rating, COUNT(*) FROM feedback GROUP BY rating")
            feedback_counts = {row[0]: row[1] for row in cursor.fetchall()}

            return {
                "total_messages": total_messages,
                "total_sessions": total_sessions,
                "avg_latency_ms": round(avg_latency, 2),
                "feedback_counts": feedback_counts
            }
