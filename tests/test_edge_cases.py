from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    original_state = deepcopy(app_module.activities)
    test_client = TestClient(app_module.app)
    yield test_client
    app_module.activities.clear()
    app_module.activities.update(original_state)


def test_signup_requires_email_parameter(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422


def test_delete_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missingstudent@example.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"


def test_delete_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@example.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
