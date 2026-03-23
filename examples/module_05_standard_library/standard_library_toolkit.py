"""Standard library example for module 5.

这个 example 把几个后端开发里最常见的标准库组合到一个真实小场景里：
导出任务快照。
"""

from __future__ import annotations

from dataclasses import asdict  # `dataclasses` 是标准库里的数据类模块；`asdict` 会把 dataclass 实例变成普通字典，方便写入 JSON。
from dataclasses import dataclass  # `dataclass` 用来快速定义结构稳定的数据对象，减少手写构造函数等样板代码。
from datetime import UTC  # `datetime` 模块负责日期时间处理；`UTC` 是一个明确的时区对象，表示“这是 UTC 时间”。
from datetime import datetime  # `datetime` 类用来获取当前时间，并把它格式化成 ISO 字符串。
from enum import StrEnum  # `enum` 模块用来定义枚举；`StrEnum` 让枚举成员天然就是字符串，写 JSON 时更直观。
import json  # `json` 是标准库里的 JSON 工具，这里用它把导出数据写成结构化文本文件。
import logging  # `logging` 是标准库日志系统，比 `print` 更适合工程代码记录运行行为。
from pathlib import Path  # `pathlib` 是标准库里的路径工具；`Path` 用来处理目录和文件路径，比拼字符串更安全。
from uuid import uuid4  # `uuid` 模块负责生成唯一标识；`uuid4()` 适合做导出文件名，避免不同导出互相覆盖。


logger = logging.getLogger(__name__)


class TaskPriority(StrEnum):
    """A tiny enum that constrains priority values to a fixed set."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(slots=True)
class TaskRecord:
    """A lightweight task object used by the export function."""

    title: str
    owner: str
    priority: TaskPriority


def export_task_snapshot(tasks: list[TaskRecord], output_dir: Path) -> Path:
    """Export one task snapshot JSON file.

    这个函数同时演示：
    - `Path.mkdir()` 创建目录
    - `uuid4()` 生成唯一文件名
    - `datetime.now(UTC)` 记录导出时间
    - `json.dumps()` 写结构化文本
    - `logging` 记录导出行为
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    # `uuid4().hex` 会生成一个几乎不重复的字符串，
    # 很适合拼到文件名里，让每次导出都保留历史结果。
    export_path = output_dir / f"task-snapshot-{uuid4().hex}.json"
    payload = {
        "exported_at": datetime.now(UTC).isoformat(),
        "tasks": [asdict(task) for task in tasks],
    }

    # `Path.write_text(...)` 是 `Path` 的便捷方法，
    # 可以直接把字符串写进文件。
    export_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info("Exported %s tasks to %s", len(tasks), export_path)
    return export_path
