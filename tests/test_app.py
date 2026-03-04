
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Test GET /activities

def test_get_activities():
    # Arrange
    # (Nessuna preparazione necessaria, dati in memoria)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test POST /activities/{activity}/signup?email=...

def test_signup_success():
    # Arrange
    email = "test1@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json().get("message", "")


def test_signup_duplicate():
    # Arrange
    email = "test2@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")


def test_signup_activity_not_found():
    # Arrange
    email = "test3@mergington.edu"
    activity = "Nonexistent"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")

# Test DELETE /activities/{activity}/participants/{email}

def test_delete_participant():
    # Arrange
    email = "test4@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert response.status_code in (200, 204, 202)  # dipende dall'implementazione


def test_delete_participant_not_found():
    # Arrange
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert response.status_code in (404, 400)
