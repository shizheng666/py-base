"""FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI  # `FastAPI` 是整个 Web 应用的核心对象，类似一个带强类型和文档能力的应用容器。

from app.api.routes import register_routes
from app.core.settings import get_settings
from app.db.session import create_session_factory
from app.models.base import Base


def create_app() -> FastAPI:
    """Create and configure a FastAPI application instance."""

    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    session_factory = create_session_factory(settings.database_url)
    app.state.session_factory = session_factory

    # 这里先通过 session_factory 取到 engine，再创建表。
    # 在教学阶段这样做更直接；后面学 Alembic 时会再升级成显式迁移。
    Base.metadata.create_all(bind=session_factory.kw["bind"])

    register_routes(app)
    return app


app = create_app()

