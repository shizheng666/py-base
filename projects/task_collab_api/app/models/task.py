"""SQLAlchemy task model."""

from __future__ import annotations

from datetime import UTC  # `UTC` 是标准库里对协调世界时的显式表示，推荐和 `datetime.now()` 配合使用来得到带时区的时间。
from datetime import datetime  # `datetime` 来自标准库，后端里经常用来记录创建时间、更新时间、截止时间。

from sqlalchemy import DateTime  # `DateTime` 告诉 SQLAlchemy 这个字段映射到数据库里的日期时间类型。
from sqlalchemy import ForeignKey  # `ForeignKey` 用来声明外键，让任务记录可以指向所属用户。
from sqlalchemy import Integer  # `Integer` 表示整数列。
from sqlalchemy import String  # `String` 表示字符串列。
from sqlalchemy.orm import Mapped  # `Mapped` 是 SQLAlchemy 2.x 的类型标注方式，表示“这个属性会被 ORM 映射”。
from sqlalchemy.orm import mapped_column  # `mapped_column` 用来声明 ORM 模型字段，相当于字段定义入口。
from sqlalchemy.orm import relationship  # `relationship` 负责 ORM 层对象关联，让我们可以通过 `task.owner` 访问用户对象。

from app.models.base import Base


class Task(Base):
    """A minimal task table used across the tutorial."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="todo", nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    owner = relationship("User", back_populates="tasks")
