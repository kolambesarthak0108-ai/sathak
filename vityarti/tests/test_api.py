"""
Integration tests for Flask REST API endpoints.
"""
import pytest
import json
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"CampusMind AI" in response.data


def test_report_page(client):
    response = client.get("/report")
    assert response.status_code == 200
    assert b"VITyarthi - Build Your Own Project" in response.data


def test_api_chat_success(client):
    payload = {"message": "When are the exams?", "session_id": "test_api_sess"}
    response = client.post(
        "/api/chat",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "response" in data
    assert data["intent"] == "exam_schedule"
    assert "latency_ms" in data


def test_api_chat_empty_message(client):
    payload = {"message": ""}
    response = client.post(
        "/api/chat",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_api_analytics_endpoint(client):
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.get_json()
    assert "runtime" in data
    assert "database" in data


def test_api_courses_endpoint(client):
    response = client.get("/api/courses")
    assert response.status_code == 200
    data = response.get_json()
    assert "courses" in data
    assert len(data["courses"]) >= 4
