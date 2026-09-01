from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def setup_function():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Science Club": {
                "description": "Conduct experiments and explore STEM topics",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 20,
                "participants": [],
            },
        }
    )


def test_unregister_participant_removes_email_from_activity():
    response = client.delete(
        "/activities/Chess Club/participants?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"


def test_unregister_missing_participant_returns_error():
    response = client.delete(
        "/activities/Science Club/participants?email=missing@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
