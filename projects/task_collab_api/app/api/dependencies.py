"""Reusable FastAPI dependencies.

依赖函数非常适合放在独立文件里，因为它们会被多个路由共享：
- 数据库会话
- 当前登录用户
- 配置对象
"""

from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends  # `Depends` 用于把一个依赖声明为另一个依赖的前置条件。
from fastapi import FastAPI
from fastapi import HTTPException  # `HTTPException` 是 FastAPI 用来返回明确 HTTP 错误的标准方式。
from fastapi import Request  # `Request` 让我们读取原始请求头、Cookie 等信息。
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

import jwt

from app.core.security import decode_access_token
from app.core.settings import Settings
from app.models.user import User
from app.services.auth_service import AuthService


def build_session_dependency(app: FastAPI):
    """Create one request-scoped database session dependency."""

    def get_session() -> Generator[Session, None, None]:
        session_factory: sessionmaker[Session] = app.state.session_factory
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    return get_session


def build_current_user_dependency(app: FastAPI):
    """Create a dependency that resolves the authenticated user from a bearer token."""

    get_session = build_session_dependency(app)

    def get_current_user(
        request: Request,
        session: Session = Depends(get_session),
    ) -> User:
        authorization = request.headers.get("Authorization", "")
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication credentials were not provided",
            )

        token = authorization.removeprefix("Bearer ").strip()

        settings: Settings = app.state.settings

        try:
            payload = decode_access_token(token, settings.jwt_secret_key)
        except jwt.PyJWTError as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token",
            ) from error

        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token subject is missing",
            )

        user = AuthService(session).get_user_by_email(subject)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found for token subject",
            )

        return user

    return get_current_user
