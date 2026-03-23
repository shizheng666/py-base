"""Authentication-related business logic."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.core.security import verify_password
from app.models.user import User
from app.schemas.user import UserLogin
from app.schemas.user import UserRegister


class AuthService:
    """Service responsible for user registration and credential verification."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def register_user(self, payload: UserRegister) -> User:
        """Create a new user if the email is still available."""

        existing_user = self.get_user_by_email(payload.email.strip().lower())
        if existing_user is not None:
            raise ValueError("email is already registered")

        user = User(
            email=payload.email.strip().lower(),
            full_name=payload.full_name.strip(),
            password_hash=hash_password(payload.password),
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def authenticate_user(self, payload: UserLogin) -> User | None:
        """Return the user when the credentials are correct."""

        user = self.get_user_by_email(payload.email.strip().lower())
        if user is None:
            return None

        if not verify_password(payload.password, user.password_hash):
            return None

        return user

    def get_user_by_email(self, email: str) -> User | None:
        """Fetch one user by email."""

        statement = select(User).where(User.email == email)
        return self.session.scalar(statement)
