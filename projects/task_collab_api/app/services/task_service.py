"""Task business logic.

这里刻意把数据库操作包成服务层，
是为了让路由函数保持轻量，也方便后续加入权限、日志和异步通知。
"""

from __future__ import annotations

from sqlalchemy import select  # `select` 是 SQLAlchemy 2.x 查询入口，等价于“我要构造一个查询表达式”。
from sqlalchemy.orm import Session  # `Session` 在服务层里代表一次数据库工作单元。

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate


class TaskService:
    """Service object responsible for task-related use cases."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def list_tasks(self, owner: User) -> list[Task]:
        """Return all tasks sorted by primary key."""

        statement = select(Task).where(Task.owner_id == owner.id).order_by(Task.id)
        return list(self.session.scalars(statement))

    def create_task(self, payload: TaskCreate, owner: User) -> Task:
        """Persist one new task and return the ORM object.

        注意这里接收的是 `TaskCreate`，不是裸字典：
        - 说明边界层已经做过一次结构化校验
        - 服务层可以更聚焦业务动作
        """

        task = Task(
            title=payload.title.strip(),
            description=payload.description.strip(),
            priority=payload.priority,
            owner_id=owner.id,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
