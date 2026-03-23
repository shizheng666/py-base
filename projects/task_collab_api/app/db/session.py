"""Database session helpers based on SQLAlchemy 2.x."""

from __future__ import annotations

from collections.abc import Generator  # `Generator` 用来标注 yield 型函数的返回类型，这类函数常用于依赖注入。

from sqlalchemy import create_engine  # `create_engine` 负责创建数据库连接引擎，是 SQLAlchemy 访问数据库的起点。
from sqlalchemy.orm import Session  # `Session` 表示一次数据库会话，承担查询、插入、提交等工作。
from sqlalchemy.orm import sessionmaker  # `sessionmaker` 用来生成 Session 工厂，避免在各处手写会话创建逻辑。
from sqlalchemy.pool import StaticPool  # `StaticPool` 让 SQLite 内存数据库在测试期间复用同一连接，避免每次请求丢数据。


def create_sqlite_engine(database_url: str):
    """Create a SQLite engine suitable for small demos and tests."""

    connect_args = {"check_same_thread": False}
    engine_kwargs = {"connect_args": connect_args}

    if database_url.endswith(":memory:"):
        engine_kwargs["poolclass"] = StaticPool

    return create_engine(database_url, **engine_kwargs)


def create_session_factory(database_url: str) -> sessionmaker[Session]:
    """Create a session factory bound to an engine."""

    engine = create_sqlite_engine(database_url)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)


def session_dependency(session_factory: sessionmaker[Session]) -> Generator[Session, None, None]:
    """Yield one session per request.

    FastAPI 里经常把这种函数作为依赖使用：
    - 进入请求时创建会话
    - 请求结束时自动关闭
    """

    session = session_factory()
    try:
        yield session
    finally:
        session.close()

