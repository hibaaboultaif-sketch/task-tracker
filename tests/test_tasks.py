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


def test_create_task_with_tags(client):
    response = client.post(
        "/tasks",
        json={"title": "Tagged task", "tags": ["backend", "urgent"]},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["tags"] == ["backend", "urgent"]


def test_create_task_blank_tag_is_dropped(client):
    response = client.post(
        "/tasks",
        json={"title": "Task with blank tag", "tags": ["backend", "   ", ""]},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["tags"] == ["backend"]


def test_update_tags_preserved_after_unrelated_update(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Task to update", "tags": ["frontend"]},
    )
    task_id = create_response.json()["id"]

    update_response = client.patch(
        f"/tasks/{task_id}", json={"priority": "High"}
    )

    assert update_response.status_code == 200
    assert update_response.json()["tags"] == ["frontend"]
    assert update_response.json()["priority"] == "High"


def test_filter_tasks_by_tag(client):
    client.post("/tasks", json={"title": "Task A", "tags": ["backend"]})
    client.post("/tasks", json={"title": "Task B", "tags": ["frontend"]})

    response = client.get("/tasks", params={"tag": "backend"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task A"


def test_create_task_invalid_due_date_format_fails(client):
    response = client.post(
        "/tasks",
        json={"title": "Bad date task", "due_date": "01-01-2026"},
    )

    assert response.status_code == 422
    assert "due_date" in response.text.lower()


def test_overdue_detection(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Overdue task", "due_date": "2020-01-01"},
    )

    assert create_response.status_code == 201
    assert create_response.json()["is_overdue"] is True


def test_future_due_date_not_overdue(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Future task", "due_date": "2099-01-01"},
    )

    assert create_response.status_code == 201
    assert create_response.json()["is_overdue"] is False


def test_filter_overdue_only(client):
    client.post("/tasks", json={"title": "Old task", "due_date": "2020-01-01"})
    client.post("/tasks", json={"title": "Future task", "due_date": "2099-01-01"})
    client.post("/tasks", json={"title": "No date task"})

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Old task"