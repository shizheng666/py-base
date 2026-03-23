"""Background notification service for module 11.

这个服务故意选择“写本地 JSONL 文件”作为第一版通知落地方式，
因为它满足三件对学习很重要的事：
1. 不依赖 Redis、邮件服务或第三方 webhook，运行成本最低。
2. 输出结果可直接观察，便于理解“后台任务真的执行了什么”。
3. 未来可以保留同样的方法边界，平滑替换成 Celery 或 webhook。
"""

from __future__ import annotations

from datetime import UTC  # `UTC` 帮我们生成带时区的标准时间，写日志时更适合跨环境阅读和排序。
from datetime import datetime  # `datetime` 用来记录通知写入时间。
import json  # `json` 是标准库模块，这里用于把 Python 字典序列化成一行 JSON 文本。
from pathlib import Path  # `Path` 用来处理文件路径，避免手写字符串拼接路径带来的问题。


class NotificationService:
    """Write structured notification records to a JSON Lines file.

    JSON Lines 的特点是“一行一个 JSON 对象”，非常适合：
    - 追加写入
    - 测试读取
    - 后续被脚本、日志系统或队列消费者继续处理
    """

    def __init__(self, notification_log_path: str) -> None:
        self.notification_log_path = Path(notification_log_path)

    def notify_task_created(
        self,
        *,
        task_id: int,
        task_title: str,
        user_email: str,
        task_created_at: datetime,
    ) -> None:
        """Append one `task.created` notification record.

        为什么这个方法不返回值：
        - 它的职责是产生副作用，也就是把日志写进文件
        - 路由层不应该等待它计算“业务结果”
        - 后续如果迁移到 Celery，这个方法边界仍然成立
        """

        log_entry = {
            "event": "task.created",
            "task_id": task_id,
            "task_title": task_title,
            "user_email": user_email,
            "task_created_at": task_created_at.isoformat(),
            "notified_at": datetime.now(UTC).isoformat(),
        }

        # `mkdir(parents=True, exist_ok=True)` 会在目录不存在时自动创建目录。
        # 这能避免第一次运行时因为父目录缺失而写文件失败。
        self.notification_log_path.parent.mkdir(parents=True, exist_ok=True)

        # 这里使用追加模式 `"a"`，而不是覆盖模式 `"w"`。
        # 这样每一次通知都会追加到文件末尾，测试也可以清楚验证“不会覆盖历史记录”。
        with self.notification_log_path.open("a", encoding="utf-8") as notification_file:
            notification_file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
