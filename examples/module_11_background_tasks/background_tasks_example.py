"""Minimal BackgroundTasks example for module 11.

这个 example 聚焦解释一件事：
HTTP 请求已经返回成功，为什么后台副作用还能继续执行？

为了把概念讲清楚，这里使用一个极简 FastAPI 应用，
并把通知落地成 JSONL 文件，而不是一开始就接 Redis/Celery。
"""

from __future__ import annotations

from datetime import UTC  # `UTC` 用来生成统一时区的时间戳，便于日志排序和理解。
from datetime import datetime  # `datetime` 用来记录任务创建时间和通知时间。
import json  # `json` 是标准库模块，用于把字典写成一行 JSON 文本。
from pathlib import Path  # `Path` 用来处理日志文件路径，避免硬编码字符串拼路径。

from fastapi import BackgroundTasks  # `BackgroundTasks` 是 FastAPI 提供的轻量后台任务调度工具。
from fastapi import FastAPI  # `FastAPI` 是 Web 应用实例类，用来创建一个最小教学应用。
from pydantic import BaseModel  # `BaseModel` 用来定义请求体结构，让输入更清晰。
from pydantic import Field  # `Field` 用来限制字段长度和提供说明。


class DemoTaskCreate(BaseModel):
    """Payload accepted by the example endpoint."""

    title: str = Field(min_length=1, max_length=120)
    user_email: str = Field(min_length=5, max_length=255)


class NotificationLogService:
    """Write one JSON notification per line.

    这个服务故意独立出来，而不是直接在路由里 `open(...).write(...)`，
    因为我们想让学习者看到：
    - 路由层负责调度
    - 服务层负责副作用细节
    """

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)

    def write_task_created_notification(
        self,
        *,
        task_title: str,
        user_email: str,
        created_at: datetime,
    ) -> None:
        payload = {
            "event": "task.created",
            "task_title": task_title,
            "user_email": user_email,
            "created_at": created_at.isoformat(),
            "notified_at": datetime.now(UTC).isoformat(),
        }

        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as file_object:
            file_object.write(json.dumps(payload, ensure_ascii=False) + "\n")


def create_example_app(notification_log_path: str) -> FastAPI:
    """Create a tiny FastAPI app that demonstrates BackgroundTasks."""

    app = FastAPI(title="Module 11 BackgroundTasks Example")
    notification_service = NotificationLogService(notification_log_path)

    @app.post("/demo-tasks", status_code=201)
    def create_demo_task(payload: DemoTaskCreate, background_tasks: BackgroundTasks) -> dict:
        """Create a fake task and schedule the background side effect.

        这里的重点不是数据库，而是：
        - 响应可以立刻返回
        - `background_tasks.add_task(...)` 会在响应发出后执行通知函数
        - 这和“把整个请求改成 async def”不是一回事
        """

        created_at = datetime.now(UTC)

        background_tasks.add_task(
            notification_service.write_task_created_notification,
            task_title=payload.title.strip(),
            user_email=payload.user_email.strip().lower(),
            created_at=created_at,
        )

        return {
            "message": "task accepted",
            "title": payload.title.strip(),
            "user_email": payload.user_email.strip().lower(),
            "created_at": created_at.isoformat(),
        }

    return app
