from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_reports_ok() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_list_tasks() -> None:
    client = TestClient(create_app())

    create_response = client.post(
        "/tasks",
        json={
            "title": "Write the learning note",
            "description": "Explain Python imports to frontend developers",
            "priority": 2,
        },
    )

    assert create_response.status_code == 201
    body = create_response.json()
    assert body["title"] == "Write the learning note"
    assert body["description"] == "Explain Python imports to frontend developers"
    assert body["priority"] == 2
    assert body["status"] == "todo"

    list_response = client.get("/tasks")

    assert list_response.status_code == 200
    tasks = list_response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Write the learning note"


def test_create_task_returns_422_for_invalid_payload() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/tasks",
        json={
            "title": "",
            "description": "invalid title",
            "priority": 9,
        },
    )

    assert response.status_code == 422
