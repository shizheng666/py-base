from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_reports_ok() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_login_and_fetch_current_user_profile() -> None:
    client = TestClient(create_app())

    register_response = client.post(
        "/auth/register",
        json={
            "email": "alice@example.com",
            "password": "super-secret-password",
            "full_name": "Alice Chen",
        },
    )

    assert register_response.status_code == 201
    registered_user = register_response.json()
    assert registered_user["email"] == "alice@example.com"
    assert registered_user["full_name"] == "Alice Chen"

    login_response = client.post(
        "/auth/login",
        json={
            "email": "alice@example.com",
            "password": "super-secret-password",
        },
    )

    assert login_response.status_code == 200
    token_body = login_response.json()
    assert token_body["token_type"] == "bearer"
    assert token_body["access_token"]

    me_response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token_body['access_token']}"},
    )

    assert me_response.status_code == 200
    current_user = me_response.json()
    assert current_user["email"] == "alice@example.com"
    assert current_user["full_name"] == "Alice Chen"


def test_create_and_list_tasks_for_the_current_user() -> None:
    client = TestClient(create_app())

    register_response = client.post(
        "/auth/register",
        json={
            "email": "alice@example.com",
            "password": "super-secret-password",
            "full_name": "Alice Chen",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "alice@example.com",
            "password": "super-secret-password",
        },
    )
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/tasks",
        json={
            "title": "Write the learning note",
            "description": "Explain Python imports to frontend developers",
            "priority": 2,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert create_response.status_code == 201
    body = create_response.json()
    assert body["title"] == "Write the learning note"
    assert body["description"] == "Explain Python imports to frontend developers"
    assert body["priority"] == 2
    assert body["status"] == "todo"
    assert body["owner"]["email"] == "alice@example.com"

    list_response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert list_response.status_code == 200
    tasks = list_response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Write the learning note"
    assert tasks[0]["owner"]["email"] == "alice@example.com"


def test_create_task_requires_authentication() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/tasks",
        json={
            "title": "Protected task",
            "description": "must not pass without token",
            "priority": 3,
        },
    )

    assert response.status_code == 401


def test_create_task_returns_422_for_invalid_payload() -> None:
    client = TestClient(create_app())

    register_response = client.post(
        "/auth/register",
        json={
            "email": "alice@example.com",
            "password": "super-secret-password",
            "full_name": "Alice Chen",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "alice@example.com",
            "password": "super-secret-password",
        },
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/tasks",
        json={
            "title": "",
            "description": "invalid title",
            "priority": 9,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


def test_login_rejects_wrong_password() -> None:
    client = TestClient(create_app())

    register_response = client.post(
        "/auth/register",
        json={
            "email": "alice@example.com",
            "password": "super-secret-password",
            "full_name": "Alice Chen",
        },
    )
    assert register_response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": "alice@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
