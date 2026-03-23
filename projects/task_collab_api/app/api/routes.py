"""HTTP routes for the sample project."""

from __future__ import annotations

from fastapi import APIRouter  # `APIRouter` 用来把一组相关接口组织在一起，避免所有路由都挤进 main.py。
from fastapi import BackgroundTasks  # `BackgroundTasks` 是 FastAPI 提供的轻量后台任务容器，适合教学和轻量异步场景。
from fastapi import Depends  # `Depends` 是 FastAPI 的依赖注入入口，用于共享数据库会话、认证信息等。
from fastapi import HTTPException  # `HTTPException` 用来把业务错误翻译为明确的 HTTP 响应。
from fastapi import FastAPI  # `FastAPI` 是应用实例类型，这里只用于类型标注。
from fastapi import status  # `status` 提供可读性更好的 HTTP 状态码常量。
from sqlalchemy.orm import Session

from app.api.dependencies import build_current_user_dependency
from app.api.dependencies import build_session_dependency
from app.core.security import create_access_token
from app.schemas.task import TaskCreate, TaskRead
from app.schemas.user import AccessToken
from app.schemas.user import UserLogin
from app.schemas.user import UserRead
from app.schemas.user import UserRegister
from app.services.auth_service import AuthService
from app.services.notification_service import NotificationService
from app.services.task_service import TaskService


def register_routes(app: FastAPI) -> None:
    """Attach routes to a FastAPI app."""

    router = APIRouter()
    get_session = build_session_dependency(app)
    get_current_user = build_current_user_dependency(app)

    @router.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @router.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
    def register_user(payload: UserRegister, session: Session = Depends(get_session)) -> UserRead:
        service = AuthService(session)

        try:
            user = service.register_user(payload)
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error

        return UserRead.model_validate(user)

    @router.post("/auth/login", response_model=AccessToken)
    def login(payload: UserLogin, session: Session = Depends(get_session)) -> AccessToken:
        service = AuthService(session)
        user = service.authenticate_user(payload)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token = create_access_token(
            subject=user.email,
            secret_key=app.state.settings.jwt_secret_key,
        )
        return AccessToken(access_token=token)

    @router.get("/me", response_model=UserRead)
    def me(current_user=Depends(get_current_user)) -> UserRead:
        return UserRead.model_validate(current_user)

    @router.get("/tasks", response_model=list[TaskRead])
    def list_tasks(
        session: Session = Depends(get_session),
        current_user=Depends(get_current_user),
    ) -> list[TaskRead]:
        service = TaskService(session)
        return [TaskRead.model_validate(task) for task in service.list_tasks(current_user)]

    @router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
    def create_task(
        payload: TaskCreate,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session),
        current_user=Depends(get_current_user),
    ) -> TaskRead:
        service = TaskService(session)
        task = service.create_task(payload, current_user)

        # 为什么只在路由层调度后台任务：
        # - 路由层知道“这是一场 HTTP 请求”，也知道可以把副作用延后执行
        # - 服务层继续保持纯粹，只负责核心业务：创建任务
        # - 以后把 `add_task(...)` 换成 Celery 投递时，这个边界也最清晰
        notification_service = NotificationService(app.state.settings.notification_log_path)
        background_tasks.add_task(
            notification_service.notify_task_created,
            task_id=task.id,
            task_title=task.title,
            user_email=current_user.email,
            task_created_at=task.created_at,
        )

        return TaskRead.model_validate(task)

    app.include_router(router)
