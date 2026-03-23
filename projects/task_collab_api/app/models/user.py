"""SQLAlchemy user model.

这个文件开始承接模块 10 的认证和授权内容。
我们先用一个最小但真实的用户表，把注册、登录和“当前用户是谁”建立起来。
"""

from __future__ import annotations

from datetime import UTC  # `UTC` 帮我们生成带时区的 UTC 时间，推荐替代过时的 `utcnow()`。
from datetime import datetime

from sqlalchemy import DateTime  # 数据库里的日期时间列类型。
from sqlalchemy import Integer  # 数据库里的整数列类型。
from sqlalchemy import String  # 数据库里的字符串列类型。
from sqlalchemy.orm import Mapped  # SQLAlchemy 2.x 的 ORM 属性类型标注。
from sqlalchemy.orm import mapped_column  # ORM 字段声明入口。
from sqlalchemy.orm import relationship  # `relationship` 用于定义 ORM 层的对象关联，比如“一个用户拥有多个任务”。

from app.models.base import Base


class User(Base):
    """A minimal user table for registration and login."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # `relationship("Task")` 让我们在 Python 对象层面可以通过 `user.tasks`
    # 访问该用户关联的所有任务。数据库层真正建立关系的关键仍然是外键。
    tasks = relationship("Task", back_populates="owner")
