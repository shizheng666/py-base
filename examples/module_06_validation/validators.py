"""Validation example for module 6."""

from __future__ import annotations

from typing import Any  # `Any` 表示“这里接收任意类型”，常用于边界层接原始输入，再在函数内部做显式校验。


class TaskPayloadError(ValueError):
    """A custom exception for invalid task input.

    自定义异常的价值在于：
    - 调用方可以只捕获“任务输入错误”，而不是误伤所有 ValueError
    - API 层可以更容易把异常翻译成统一错误响应
    """


def validate_task_payload(payload: dict[str, Any]) -> dict[str, int | str]:
    """Validate and normalize a task-like payload.

    这类函数常处于“边界层”和“业务层”之间：
    - 边界层拿到原始输入
    - 这里负责做业务可理解的清洗与校验
    - 再把更稳定的数据结构交给后续逻辑
    """

    raw_title = payload.get("title", "")
    if not isinstance(raw_title, str) or not raw_title.strip():
        raise TaskPayloadError("title must be a non-empty string")

    raw_priority = payload.get("priority")
    if not isinstance(raw_priority, int) or not 1 <= raw_priority <= 5:
        raise TaskPayloadError("priority must be an integer between 1 and 5")

    raw_due_in_days = payload.get("due_in_days")
    if not isinstance(raw_due_in_days, int) or raw_due_in_days < 0:
        raise TaskPayloadError("due_in_days must be a non-negative integer")

    return {
        "title": raw_title.strip(),
        "priority": raw_priority,
        "due_in_days": raw_due_in_days,
    }

