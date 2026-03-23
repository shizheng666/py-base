"""Minimal FastAPI core example for module 9."""

from __future__ import annotations

from dataclasses import dataclass  # `dataclasses` 是标准库的数据类模块；`dataclass` 适合表达内存里的简单任务对象。

from fastapi import FastAPI  # `fastapi` 是 Web 框架；`FastAPI` 类用来创建应用实例，也就是整个 API 的入口对象。
from fastapi import status  # `status` 提供带语义的 HTTP 状态码常量，比如 `HTTP_201_CREATED`，比直接写数字更好读。
from pydantic import BaseModel  # `pydantic` 负责数据校验；`BaseModel` 是请求体和响应体模型的基类。
from pydantic import ConfigDict  # `ConfigDict` 用来配置 Pydantic 模型行为，这里用于允许从 dataclass 读取属性。
from pydantic import Field  # `Field` 用来声明字段约束，比如最小长度、默认值、取值范围。


@dataclass(slots=True)
class DemoTask:
    """A tiny in-memory task object.

    这个对象不是数据库模型，也不是 HTTP 请求体，
    它只是应用内部暂存的一份数据。
    """

    id: int
    title: str
    priority: int


class DemoTaskCreate(BaseModel):
    """Payload received from the client when creating a task."""

    title: str = Field(min_length=1, max_length=120)
    priority: int = Field(default=3, ge=1, le=5)


class DemoTaskRead(BaseModel):
    """Payload returned to the client."""

    id: int
    title: str
    priority: int

    model_config = ConfigDict(from_attributes=True)


def create_example_app() -> FastAPI:
    """Create a tiny FastAPI app with one health endpoint and one task resource."""

    app = FastAPI(title="Module 09 FastAPI Core Example")

    # 这里直接用内存列表保存任务，目的是把学习重点放在 FastAPI 核心概念上，
    # 而不是提前引入数据库。
    demo_tasks: list[DemoTask] = []

    @app.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/demo-tasks", response_model=list[DemoTaskRead])
    def list_demo_tasks() -> list[DemoTaskRead]:
        # `response_model=...` 的价值在于：
        # 1. 自动校验返回结构
        # 2. 自动出现在 OpenAPI 文档里
        return [DemoTaskRead.model_validate(task) for task in demo_tasks]

    @app.post("/demo-tasks", response_model=DemoTaskRead, status_code=status.HTTP_201_CREATED)
    def create_demo_task(payload: DemoTaskCreate) -> DemoTaskRead:
        # `payload` 已经由 Pydantic 做过一次结构和范围校验，
        # 所以这里可以更专注地构造任务对象。
        task = DemoTask(
            id=len(demo_tasks) + 1,
            title=payload.title.strip(),
            priority=payload.priority,
        )
        demo_tasks.append(task)
        return DemoTaskRead.model_validate(task)

    return app
