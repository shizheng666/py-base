import json

from fastapi.testclient import TestClient

from background_tasks_example import create_example_app


def test_background_task_writes_one_notification_line(tmp_path) -> None:
    notification_log = tmp_path / "notifications.jsonl"
    client = TestClient(create_example_app(str(notification_log)))

    response = client.post(
        "/demo-tasks",
        json={
            "title": "Learn BackgroundTasks",
            "user_email": "alice@example.com",
        },
    )

    assert response.status_code == 201
    assert notification_log.exists()

    lines = notification_log.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1

    payload = json.loads(lines[0])
    assert payload["event"] == "task.created"
    assert payload["task_title"] == "Learn BackgroundTasks"
    assert payload["user_email"] == "alice@example.com"


def test_background_task_appends_notifications_instead_of_overwriting(tmp_path) -> None:
    notification_log = tmp_path / "notifications.jsonl"
    client = TestClient(create_example_app(str(notification_log)))

    for task_title in ["First task", "Second task"]:
        response = client.post(
            "/demo-tasks",
            json={
                "title": task_title,
                "user_email": "alice@example.com",
            },
        )
        assert response.status_code == 201

    lines = notification_log.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2

    first_payload = json.loads(lines[0])
    second_payload = json.loads(lines[1])
    assert first_payload["task_title"] == "First task"
    assert second_payload["task_title"] == "Second task"
