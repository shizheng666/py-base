# 模块 9：FastAPI 核心开发

## 学习目标

- 能写路由、请求参数、响应模型和异常处理
- 理解依赖注入、Pydantic 校验和 OpenAPI 文档
- 能把前面的语言基础迁移到真实 API 代码里

## 核心概念

- 路由层只做输入输出协调，不堆业务逻辑
- `Pydantic` 负责边界校验，不替代数据库模型
- 依赖注入适合共享数据库会话、认证上下文和服务对象

## 主项目应用

本章开始重点阅读 `projects/task_collab_api/app/`：

- `main.py`：应用入口
- `api/routes.py`：路由定义
- `schemas/task.py`：请求响应模型
- `services/task_service.py`：业务逻辑

## 与前端对照

- FastAPI 像“更现代、更类型友好的 Express/NestJS 混合体”
- `response_model` 接近“接口返回 DTO 契约”

## 常用库

- `FastAPI`
- `Uvicorn`
- `Pydantic`

## 实战任务

- 增加一个 `GET /tasks` 过滤参数
- 给任务创建接口补失败用例
- 观察自动生成的 OpenAPI 文档
