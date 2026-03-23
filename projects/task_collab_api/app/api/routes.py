"""HTTP routes for the sample project."""

from __future__ import annotations

from collections.abc import Generator  # 用于标注依赖函数的 yield 类型。

from fastapi import APIRouter  # `APIRouter` 用来把一组相关接口组织在一起，避免所有路由都挤进 main.py。
from fastapi import Depends  # `Depends` 是 FastAPI 的依赖注入入口，用于共享数据库会话、认证信息等。
from fastapi import FastAPI  # `FastAPI` 是应用实例类型，这里只用于类型标注。
from fastapi import status  # `status` 提供可读性更好的 HTTP 状态码常量。
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.schemas.task import TaskCreate, TaskRead
from app.services.task_service import TaskService


router = APIRouter()


def build_session_dependency(app: FastAPI):
    """Create a dependency function bound to the current app.

    为什么不用全局变量：
    - 这样每个 app 实例都能带自己的数据库配置
    - 测试时可以创建干净的应用实例
    """

    def get_session() -> Generator[Session, None, None]:
        session_factory: sessionmaker[Session] = app.state.session_factory
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    return get_session


def register_routes(app: FastAPI) -> None:
    """Attach routes to a FastAPI app."""

    get_session = build_session_dependency(app)

    @router.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/tasks", response_model=list[TaskRead])
    def list_tasks(session: Session = Depends(get_session)) -> list[TaskRead]:
        service = TaskService(session)
        return [TaskRead.model_validate(task) for task in service.list_tasks()]

    @router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
    def create_task(payload: TaskCreate, session: Session = Depends(get_session)) -> TaskRead:
        service = TaskService(session)
        task = service.create_task(payload)
        return TaskRead.model_validate(task)

    app.include_router(router)

