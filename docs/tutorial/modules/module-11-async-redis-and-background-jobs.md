# 模块 11：异步编程、Redis 与后台任务

## 学习目标

- 理解 Python 里的协程、事件循环和 I/O 密集型场景
- 能区分“接口立即返回”和“后台异步处理”
- 看懂 Redis、任务队列和简单通知流程

## 核心概念

- `async/await` 不是自动变快，而是让 I/O 等待更高效
- 后台任务适合邮件、通知、批处理、定时任务
- Redis 常作为缓存、消息中间件或任务队列依赖

## 与前端对照

- JS 和 Python 都有 `async/await`
- 但它们背后的生态、服务器模型和并发边界不完全一样

## 主项目应用

- 新建一个任务后异步发送通知
- 让后台任务和 API 进程解耦

## 第一版实现策略

本教程第一版不会直接上 Redis/Celery，而是先使用 `FastAPI BackgroundTasks`。
这样做的原因是：

- 学习成本更低，可以先专注理解“请求已经返回，但后台逻辑仍在继续”
- 不需要先安装额外服务，就能看到异步行为
- 后续依然可以把同一条通知边界升级到消息队列

## 代码阅读建议

建议按下面顺序阅读：

1. `examples/module_11_background_tasks/background_tasks_example.py`
2. `examples/module_11_background_tasks/test_background_tasks_example.py`
3. `projects/task_collab_api/app/api/routes.py`
4. `projects/task_collab_api/app/services/notification_service.py`
5. `projects/task_collab_api/tests/test_api.py`

先看 example 里最小的 `BackgroundTasks` 行为，再看主项目里它如何接入真实任务创建流程。

## 运行与验证

```powershell
uv run pytest projects/task_collab_api/tests -q
uv run pytest examples/module_11_background_tasks -q
uv run python examples/module_11_background_tasks/demo_background_tasks.py
uv run uvicorn projects.task_collab_api.app.main:app --reload
Get-Content projects/task_collab_api/runtime/notifications.jsonl
```

## 从 BackgroundTasks 升级到 Redis/Celery 的思路

- 当前：`background_tasks.add_task(notification_service.notify_task_created, ...)`
- 升级后：把这里替换为消息投递或 Celery task 调用
- 当前通知输出：本地 JSONL 文件
- 升级后输出：webhook、邮件、消息队列消费者、审计日志系统

## 常用库

- `httpx`
- `redis`
- `Celery`
