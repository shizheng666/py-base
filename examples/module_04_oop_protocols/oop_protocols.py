"""OOP and protocol-based design example for module 4.

这个 example 想讲清楚一件事：
在 Python 里，很多时候我们更关心“对象能不能完成某个行为”，
而不是它是不是某个继承体系里的子类。
"""

from __future__ import annotations

from dataclasses import asdict  # `dataclasses` 是标准库里的“数据类”模块；`asdict` 会把 dataclass 实例转换成普通字典，方便后续继续做 JSON 序列化。
from dataclasses import dataclass  # `dataclass` 是一个装饰器；它会自动帮类生成 `__init__`、`__repr__` 等样板方法，非常适合“以数据为主”的小对象。
import json  # `json` 是标准库里的 JSON 处理模块；这里我们用它把任务对象输出成 JSON 字符串。
from typing import Protocol  # `typing` 是标准库里的类型提示模块；`Protocol` 用来表达“只要实现了这个方法集合，就能被当成这个类型使用”。


@dataclass(slots=True)
class Task:
    """A simple task object used by the presenters.

    这里的字段故意保持简单，
    是为了把注意力集中在“对象如何协作”而不是复杂业务属性上。
    """

    title: str
    status: str
    owner: str


class TaskFormatter(Protocol):
    """Any object that provides `format_task` can be used by TaskPresenter.

    这就是协议式设计的关键：
    - 不强迫所有 formatter 继承同一个基类
    - 只要求它们实现一致的方法签名
    - 这样 TaskPresenter 就能接收“任何符合协议的对象”
    """

    def format_task(self, task: Task) -> str:
        """Format one task into a string."""


class PlainTextTaskFormatter:
    """Render a task as a short plain-text line."""

    def format_task(self, task: Task) -> str:
        # 纯文本 formatter 适合终端输出、日志、CLI 工具等场景。
        return f"[{task.status}] {task.title} -> {task.owner}"


class JsonTaskFormatter:
    """Render a task as a JSON string."""

    def format_task(self, task: Task) -> str:
        # `asdict(task)` 先把 dataclass 对象变成普通字典，
        # `json.dumps(...)` 再把字典序列化成字符串。
        return json.dumps(asdict(task), ensure_ascii=False, sort_keys=True)


class TaskPresenter:
    """Compose a formatter instead of inheriting multiple presenter types.

    这里的重点是“组合”：
    - presenter 负责组织展示流程
    - formatter 负责决定输出格式
    - 两者通过协议解耦
    """

    def __init__(self, formatter: TaskFormatter) -> None:
        # 把 formatter 作为依赖注入进来，而不是写死在类内部，
        # 这样 presenter 就可以在运行时切换格式化策略。
        self.formatter = formatter

    def present(self, task: Task) -> str:
        return self.formatter.format_task(task)
