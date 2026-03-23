FROM python:3.12-slim

WORKDIR /app

# 先复制依赖声明，便于 Docker 层缓存。
COPY pyproject.toml README.md /app/
COPY projects/task_collab_api /app/projects/task_collab_api

RUN pip install --no-cache-dir uv && uv pip install --system .

EXPOSE 8000

CMD ["uvicorn", "projects.task_collab_api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

