# Task Collaboration API

这是教程主项目的第一版骨架，用来承接模块 7-12 的内容。

## 当前已实现

- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `GET /me`
- `GET /tasks`
- `POST /tasks`
- `POST /tasks` 创建成功后会触发一个后台通知任务
- SQLite 内存数据库
- SQLAlchemy 2.x ORM 模型
- Pydantic 请求与响应模型
- JWT 认证
- FastAPI `BackgroundTasks`
- pytest + FastAPI TestClient 测试

## 后续扩展方向

- 用户注册与登录
- JWT 鉴权
- 任务评论和标签
- Redis / Celery 后台任务
- Docker Compose 和 PostgreSQL

## 如何观察异步通知

模块 11 的第一版不会直接接 Redis/Celery，而是先把通知写入本地 JSONL 文件。
这样你可以先看清“请求返回”和“后台副作用”是怎么分开的。

默认输出文件由 `NOTIFICATION_LOG_PATH` 控制，示例值在 `.env.example` 里。

创建任务后，可以直接查看日志：

```powershell
Get-Content projects/task_collab_api/runtime/notifications.jsonl
```

每一行都是一条独立通知，至少包含：

- `event`
- `task_id`
- `task_title`
- `user_email`
- `task_created_at`
- `notified_at`

## 启动方式

```powershell
uv run uvicorn projects.task_collab_api.app.main:app --reload
```

## 运行测试

```powershell
uv run pytest projects/task_collab_api/tests -q
```
