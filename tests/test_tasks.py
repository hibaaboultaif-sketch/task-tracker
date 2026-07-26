import app.main as main
from app.main import app
from fastapi.testclient import TestClient
import pytest


@pytest.fixture(autouse=True)
def reset_task_storage():
    main.tasks.clear()
    main.next_task_id = 1


@pytest.fixture
def client():
    return TestClient(app)


def test_create_task_success(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Add pytest coverage",
            "priority": "High",
            "assignee": "dev",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Write tests"
    assert data["description"] == "Add pytest coverage"
    assert data["status"] == "ToDo"
    assert data["priority"] == "High"
    assert data["assignee"] == "dev"


def test_create_task_blank_title_fails(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422
    assert "title" in response.text.lower()


def test_get_task_not_found(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_valid_status_transition(client):
    create_response = client.post("/tasks", json={"title": "Status flow task"})
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    in_progress_response = client.patch(
        f"/tasks/{task_id}", json={"status": "InProgress"}
    )
    assert in_progress_response.status_code == 200
    assert in_progress_response.json()["status"] == "InProgress"

    done_response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert done_response.status_code == 200
    assert done_response.json()["status"] == "Done"


def test_invalid_status_transition_rejected(client):
    create_response = client.post("/tasks", json={"title": "Invalid transition task"})
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]
    assert create_response.json()["status"] == "ToDo"

    response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})

    assert response.status_code == 422
    detail = response.json()["detail"].lower()
    assert "invalid" in detail or "transition" in detail


def test_delete_task(client):
    create_response = client.post("/tasks", json={"title": "Task to delete"})
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Task not found"
