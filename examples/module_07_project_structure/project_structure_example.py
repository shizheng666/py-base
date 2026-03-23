"""Project structure example for module 7.

模块 7 的核心不是某个库 API，而是“在动手实现前先把边界想清楚”。
这个 example 用一个轻量的计划对象来展示：
- 哪些文件负责输入输出
- 哪些文件负责业务逻辑
- 哪些文件负责 HTTP 入口
"""

from __future__ import annotations

from dataclasses import dataclass  # `dataclasses` 是标准库里的数据类模块；`dataclass` 适合把“计划项”“配置项”这类结构化信息写得清楚又简洁。


@dataclass(slots=True)
class FeaturePlan:
    """A tiny structure describing file responsibilities for one feature."""

    # `feature_name` 表示我们当前讨论的是哪个业务能力。
    feature_name: str
    # `files_by_role` 的 key 是职责名，value 是建议文件名。
    # 这样学习者能看到“职责 -> 文件”的映射，而不是只看到零散路径。
    files_by_role: dict[str, str]


def build_task_feature_plan() -> FeaturePlan:
    """Return a teaching-friendly plan for a task feature.

    这不是代码生成器，而是一个“先想边界，再写代码”的最小例子。
    """

    return FeaturePlan(
        feature_name="task feature",
        files_by_role={
            "http_entry": "routes.py",
            "input_output": "schemas.py",
            "business_logic": "services.py",
            "persistence": "models.py",
        },
    )


def quality_commands() -> list[str]:
    """Return the core verification commands for a small Python project."""

    # 这里返回字符串列表，是因为模块 7 关注的是“工程约定”，
    # 而不是在 example 里真的去执行这些命令。
    return [
        "uv run pytest -q",
        "uv run ruff check .",
        "uv run mypy .",
    ]
