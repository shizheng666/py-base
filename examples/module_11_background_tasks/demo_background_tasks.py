"""A tiny runnable script for module 11."""

import json
from pathlib import Path
import tempfile

from fastapi.testclient import TestClient

from background_tasks_example import create_example_app


def main() -> None:
    with tempfile.TemporaryDirectory() as temp_directory:
        log_path = Path(temp_directory) / "notifications.jsonl"
        client = TestClient(create_example_app(str(log_path)))

        response = client.post(
            "/demo-tasks",
            json={
                "title": "Watch background task behavior",
                "user_email": "alice@example.com",
            },
        )

        print("response status:", response.status_code)
        print("response body:", response.json())

        latest_line = log_path.read_text(encoding="utf-8").splitlines()[-1]
        print("notification line:", json.loads(latest_line))


if __name__ == "__main__":
    main()
