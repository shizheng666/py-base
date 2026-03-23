"""A tiny runnable script for module 10."""

from auth_flow import SimpleUserStore
from auth_flow import decode_token_for_learning
from auth_flow import login_user
from auth_flow import register_user


def main() -> None:
    store = SimpleUserStore()
    user = register_user(
        store,
        email="alice@example.com",
        password="super-secret-password",
        full_name="Alice Chen",
    )
    print("registered user:", user)

    login_result = login_user(
        store,
        email="alice@example.com",
        password="super-secret-password",
    )
    print("login result:", login_result)

    token_payload = decode_token_for_learning(login_result["access_token"])
    print("decoded token payload:", token_payload)


if __name__ == "__main__":
    main()
