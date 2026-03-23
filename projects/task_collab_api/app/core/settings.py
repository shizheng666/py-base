"""Project settings.

这个文件负责集中管理配置，而不是把数据库地址或环境变量散落在各处。
"""

from __future__ import annotations

from pydantic import Field  # `Field` 用来为配置字段提供默认值和元数据说明。
from pydantic_settings import BaseSettings  # `BaseSettings` 会把环境变量映射到 Python 对象，非常适合管理配置。
from pydantic_settings import SettingsConfigDict  # `SettingsConfigDict` 用来配置 BaseSettings 的行为，比如 env 文件名。


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = Field(default="Task Collaboration API")
    database_url: str = Field(default="sqlite+pysqlite:///:memory:")
    redis_url: str = Field(default="redis://localhost:6379/0")
    debug: bool = Field(default=True)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    """Return a fresh settings object.

    真实生产项目里可以进一步做缓存，
    这里保持简单，方便教学时理解“配置对象从哪里来”。
    """

    return Settings()

