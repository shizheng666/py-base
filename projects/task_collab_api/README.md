# Task Collaboration API

这是教程主项目的第一版骨架，用来承接模块 7-12 的内容。

## 当前已实现

- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `GET /me`
- `GET /tasks`
- `POST /tasks`
- SQLite 内存数据库
- SQLAlchemy 2.x ORM 模型
- Pydantic 请求与响应模型
- JWT 认证
- pytest + FastAPI TestClient 测试

## 后续扩展方向

- 用户注册与登录
- JWT 鉴权
- 任务评论和标签
- Redis / Celery 后台任务
- Docker Compose 和 PostgreSQL

## 启动方式

```powershell
uv run uvicorn projects.task_collab_api.app.main:app --reload
```

## 运行测试

```powershell
uv run pytest projects/task_collab_api/tests -q
```
