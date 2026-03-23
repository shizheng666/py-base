"""Typing and dataclass example for module 3."""

from __future__ import annotations

from dataclasses import dataclass  # `dataclass` 来自标准库 `dataclasses`，主要用于快速定义“以数据为主”的类。
from typing import Literal  # `Literal` 来自 `typing`，用于把字符串取值限制在固定集合里，编辑器和类型检查器会更聪明。


TaskStatus = Literal["todo", "doing", "done"]


@dataclass(slots=True)
class TaskSummary:
    """A small, stable data object.

    这个类适合用 dataclass，因为它主要是“承载数据”，
    不是带大量复杂行为的领域对象。

    `slots=True` 的作用：
    - 限制实例可拥有的属性集合
    - 降低一些内存开销
    - 防止手滑给对象挂上不存在的新属性
    """

    title: str
    status: TaskStatus
    owner: str


def build_task_summary(title: str, status: TaskStatus, owner: str) -> TaskSummary:
    """Create a typed task summary object.

    这个函数看起来很简单，但它体现了一个重要习惯：
    让“构造和规范化数据”的工作集中在明确边界里完成。
    """

    return TaskSummary(title=title.strip(), status=status, owner=owner.strip())


def status_label(status: TaskStatus) -> str:
    """Translate machine-friendly status into human-friendly text.

    `match-case` 是 Python 3.10 新增的结构化匹配语法。
    这里用它是因为状态分支是固定且可枚举的。
    """

    match status:
        case "todo":
            return "Not started"
        case "doing":
            return "In progress"
        case "done":
            return "Completed"
        case _:
            raise ValueError(f"Unsupported status: {status}")

