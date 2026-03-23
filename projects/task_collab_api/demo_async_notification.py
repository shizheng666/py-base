"""Small demo script for module 11.

这个脚本不是为了替代 pytest，而是为了让学习者在终端里亲眼看到：
1. 注册和登录拿到 token
2. 创建任务后接口立即返回
3. 后台通知把 JSONL 日志写到磁盘

脚本保持同步风格，目的是先把“请求流程”和“通知结果”讲清楚。
后面讲 `httpx.AsyncClient` 时，再升级到真正的异步客户端写法。
"""

from __future__ import annotations

import json  # 用来把日志文件中的每一行 JSON 文本转回 Python 字典。
from pathlib import Path  # `Path` 让读取通知日志文件更直观。

from fastapi.testclient import TestClient  # `TestClient` 让我们在不启动独立服务器的情况下直接调用 FastAPI 应用。

from app.main import create_app


def main() -> None:
    app = create_app()
    client = TestClient(app)

    register_response = client.post(
        "/auth/register",
        json={
            "email": "demo@example.com",
            "password": "super-secret-password",
            "full_name": "Demo User",
        },
    )
    print("register status:", register_response.status_code)

    login_response = client.post(
        "/auth/login",
        json={
            "email": "demo@example.com",
            "password": "super-secret-password",
        },
    )
    print("login status:", login_response.status_code)

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/tasks",
        json={
            "title": "Watch async notification",
            "description": "Observe the JSONL notification output",
            "priority": 2,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    print("create task status:", create_response.status_code)
    print("task response:", create_response.json())

    notification_log_path = Path(app.state.settings.notification_log_path)
    print("notification log path:", notification_log_path)

    if notification_log_path.exists():
        last_line = notification_log_path.read_text(encoding="utf-8").splitlines()[-1]
        print("latest notification:", json.loads(last_line))
    else:
        print("notification log not found yet")


if __name__ == "__main__":
    main()
