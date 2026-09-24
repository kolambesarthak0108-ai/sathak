"""
Application Entry Point: app.py
CampusMind AI – College & Academic Assistant Web Server & REST API.
"""
import time
import uuid
import os
from flask import Flask, render_template, request, jsonify, send_from_directory

from core.dialogue_manager import DialogueManager
from core.analytics import AnalyticsTracker
from models.database import DatabaseManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates")
)

# Instantiate core subsystems
dialogue_mgr = DialogueManager()
analytics = AnalyticsTracker()
db = DatabaseManager()


@app.route("/")
def index():
    """Render the main conversational web application."""
    return render_template("index.html")


@app.route("/report")
def project_report():
    """Render the comprehensive 15-section academic project report."""
    return render_template("report.html")


@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
    """
    Process incoming user message.
    Payload: { "message": str, "session_id": Optional[str] }
    """
    start_time = time.perf_counter()
    data = request.get_json(force=True, silent=True) or {}
    user_message = data.get("message", "").strip()
    session_id = data.get("session_id") or str(uuid.uuid4())

    if not user_message:
        return jsonify({
            "error": "Empty message received",
            "status": "bad_request"
        }), 400

    # Process through dialogue manager
    result = dialogue_mgr.process_message(session_id, user_message)

    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
    result["latency_ms"] = latency_ms

    # Telemetry and logging
    analytics.record_query(result["intent"], latency_ms)
    log_id = db.log_interaction(
        session_id=session_id,
        user_message=user_message,
        bot_response=result["response"],
        intent=result["intent"],
        confidence=result["confidence"],
        latency_ms=latency_ms
    )
    result["message_id"] = log_id

    return jsonify(result)


@app.route("/api/history/<session_id>", methods=["GET"])
def history_endpoint(session_id: str):
    """Retrieve chat history for a session."""
    history = db.get_session_history(session_id)
    return jsonify({
        "session_id": session_id,
        "count": len(history),
        "history": history
    })


@app.route("/api/feedback", methods=["POST"])
def feedback_endpoint():
    """
    Record user feedback on bot answers.
    Payload: { "session_id": str, "rating": "positive"|"negative", "comment": Optional[str] }
    """
    data = request.get_json(force=True, silent=True) or {}
    session_id = data.get("session_id", "anonymous")
    rating = data.get("rating", "positive")
    comment = data.get("comment", "")

    analytics.record_feedback(rating)
    db.save_feedback(session_id, rating, comment)

    return jsonify({
        "status": "success",
        "message": "Feedback recorded successfully"
    })


@app.route("/api/analytics", methods=["GET"])
def analytics_endpoint():
    """Return runtime metrics and aggregated database statistics."""
    runtime_metrics = analytics.get_metrics()
    db_stats = db.get_summary_stats()
    return jsonify({
        "runtime": runtime_metrics,
        "database": db_stats
    })


@app.route("/api/courses", methods=["GET"])
def courses_endpoint():
    """Return catalogue of available courses."""
    courses = dialogue_mgr.knowledge_base.get_all_courses()
    return jsonify({"courses": courses})


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting CampusMind AI Server at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
