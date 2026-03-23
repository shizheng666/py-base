from fastapi.testclient import TestClient

from fastapi_tasks_example import create_example_app


def test_health_endpoint_reports_ok() -> None:
    client = TestClient(create_example_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_demo_tasks() -> None:
    client = TestClient(create_example_app())

    create_response = client.post(
        "/demo-tasks",
        json={
            "title": "Learn FastAPI",
            "priority": 2,
        },
    )

    assert create_response.status_code == 201
    assert create_response.json()["title"] == "Learn FastAPI"

    list_response = client.get("/demo-tasks")

    assert list_response.status_code == 200
    payload = list_response.json()
    assert len(payload) == 1
    assert payload[0]["title"] == "Learn FastAPI"
