"""Pydantic schemas for API input and output."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel  # `BaseModel` 是 Pydantic 的核心基类，负责数据校验、类型转换和序列化。
from pydantic import ConfigDict  # `ConfigDict` 用来声明模型行为，比如能否从 ORM 对象读取字段。
from pydantic import Field  # `Field` 用来补充字段约束和描述，比如最小长度、默认值。

from app.schemas.user import UserRead


class TaskCreate(BaseModel):
    """Payload for creating a task."""

    title: str = Field(min_length=1, max_length=120, description="Task title shown to users.")
    description: str = Field(default="", max_length=500, description="Longer explanation of the task.")
    priority: int = Field(default=3, ge=1, le=5, description="1 is highest priority, 5 is lowest.")


class TaskRead(BaseModel):
    """Serialized task returned by the API."""

    id: int
    title: str
    description: str
    priority: int
    status: str
    owner: UserRead
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
