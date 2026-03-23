from auth_flow import AuthenticationError
from auth_flow import SimpleUserStore
from auth_flow import decode_token_for_learning
from auth_flow import login_user
from auth_flow import register_user


def test_register_and_login_returns_a_bearer_token() -> None:
    store = SimpleUserStore()
    register_user(
        store,
        email="alice@example.com",
        password="super-secret-password",
        full_name="Alice Chen",
    )

    login_result = login_user(
        store,
        email="alice@example.com",
        password="super-secret-password",
    )

    assert login_result["token_type"] == "bearer"
    token_payload = decode_token_for_learning(login_result["access_token"])
    assert token_payload["sub"] == "alice@example.com"


def test_login_rejects_a_wrong_password() -> None:
    store = SimpleUserStore()
    register_user(
        store,
        email="alice@example.com",
        password="super-secret-password",
        full_name="Alice Chen",
    )

    try:
        login_user(
            store,
            email="alice@example.com",
            password="wrong-password",
        )
    except AuthenticationError as error:
        assert "Invalid email or password" in str(error)
    else:
        raise AssertionError("login_user should reject the wrong password")


def test_decode_token_rejects_invalid_tokens() -> None:
    try:
        decode_token_for_learning("not-a-real-token")
    except AuthenticationError as error:
        assert "Invalid or expired token" in str(error)
    else:
        raise AssertionError("decode_token_for_learning should reject invalid tokens")
