"""Minimal SQLAlchemy 2.x example for module 8."""

from __future__ import annotations

from dataclasses import dataclass  # `dataclasses` 是标准库的数据类模块；`dataclass` 适合表示“创建任务时传入什么数据”这种轻量输入对象。

from sqlalchemy import Integer  # `sqlalchemy` 是数据库访问库；`Integer` 表示 ORM 模型里的某个列会映射成整数类型。
from sqlalchemy import String  # `String` 表示 ORM 模型里的某个列会映射成字符串类型，通常还能附带长度限制。
from sqlalchemy import create_engine  # `create_engine` 是 SQLAlchemy 连接数据库的入口，没有它 ORM 不知道该连到哪种数据库。
from sqlalchemy import select  # `select` 用来构造查询表达式，是 SQLAlchemy 2.x 里推荐的查询写法入口。
from sqlalchemy.orm import DeclarativeBase  # `sqlalchemy.orm` 是 ORM 子模块；`DeclarativeBase` 用来声明所有 ORM 模型共同继承的基类。
from sqlalchemy.orm import Mapped  # `Mapped` 是 SQLAlchemy 2.x 的类型标注工具，用来说明“这个属性会被映射成数据库列”。
from sqlalchemy.orm import Session  # `Session` 代表一次数据库会话，负责查询、插入、提交和刷新对象。
from sqlalchemy.orm import mapped_column  # `mapped_column` 用来定义 ORM 字段本身，相当于“声明一个数据库列”。
from sqlalchemy.orm import sessionmaker  # `sessionmaker` 用来创建 Session 工厂，避免每次都手动拼装 Session。
from sqlalchemy.pool import StaticPool  # `StaticPool` 让内存 SQLite 在这个示例里复用同一连接，否则每次都像新的空数据库。


class Base(DeclarativeBase):
    """Base class for the ORM example."""


class TaskRow(Base):
    """A tiny ORM model for task records."""

    __tablename__ = "demo_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)


@dataclass(slots=True)
class TaskCreate:
    """Input object used before we create the ORM row."""

    # 这里刻意把“输入对象”与 ORM 模型分开，
    # 是为了说明 API/schema 层和数据库模型层不应该天然混在一起。
    title: str
    priority: int


def make_session() -> Session:
    """Create a session bound to an in-memory SQLite database."""

    # `sqlite+pysqlite:///:memory:` 表示使用 SQLite 内存数据库。
    # 它零配置、启动快，非常适合教学和测试。
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # `Base.metadata.create_all(engine)` 会按照当前已声明的 ORM 模型把表建出来。
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, class_=Session)
    return session_factory()


def create_task(session: Session, payload: TaskCreate) -> TaskRow:
    """Insert one ORM row and return it."""

    # 这里用 `payload` 构造 ORM 模型，
    # 体现的是“输入对象 -> 持久化对象”的转换过程。
    task = TaskRow(title=payload.title.strip(), priority=payload.priority)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def list_tasks(session: Session) -> list[TaskRow]:
    """Return all rows ordered by primary key."""

    # `select(TaskRow)` 表示“查询 TaskRow 这张表/这个模型”，
    # `order_by(TaskRow.id)` 则让返回顺序稳定，测试也更容易写。
    statement = select(TaskRow).order_by(TaskRow.id)
    return list(session.scalars(statement))
