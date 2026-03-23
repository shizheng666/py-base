"""Base class for SQLAlchemy models."""

from sqlalchemy.orm import DeclarativeBase  # `DeclarativeBase` 是 SQLAlchemy 2.x 推荐的声明式模型基类写法。


class Base(DeclarativeBase):
    """All ORM models inherit from this class."""

