"""Pytest setup for the FastAPI sample project."""

from pathlib import Path  # `Path` 用来定位项目目录。
import sys  # `sys.path` 让测试能导入 `app` 包。


PROJECT_ROOT = Path(__file__).resolve().parents[1]
project_root_as_text = str(PROJECT_ROOT)

if project_root_as_text not in sys.path:
    sys.path.insert(0, project_root_as_text)

