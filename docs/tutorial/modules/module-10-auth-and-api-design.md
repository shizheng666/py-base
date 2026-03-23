# 模块 10：认证、权限与 API 设计

## 学习目标

- 理解 JWT、密码哈希和用户上下文
- 能设计分页、过滤、排序和错误码
- 知道哪些逻辑属于认证，哪些属于业务授权

## 核心概念

- 认证回答“你是谁”
- 授权回答“你能做什么”
- 接口设计要为前端联调和长期维护服务

## 主项目应用

- 增加注册和登录接口
- 在任务接口里加入用户隔离
- 统一错误响应格式
- 使用 JWT 表示登录后的用户身份
- 在依赖函数里解析 `Authorization: Bearer <token>`

## 与前端对照

- 类似前端里的 token 登录流
- 但后端必须真正校验权限边界，而不仅是隐藏按钮

## 常用库

- JWT 方案
- 密码哈希方案
- `pydantic-settings` 或等价配置方案

## 代码阅读建议

本章重点阅读这些文件：

- [user.py](C:/Users/admin/Desktop/study/py_base/projects/task_collab_api/app/models/user.py)
- [security.py](C:/Users/admin/Desktop/study/py_base/projects/task_collab_api/app/core/security.py)
- [dependencies.py](C:/Users/admin/Desktop/study/py_base/projects/task_collab_api/app/api/dependencies.py)
- [auth_service.py](C:/Users/admin/Desktop/study/py_base/projects/task_collab_api/app/services/auth_service.py)

阅读顺序建议：

1. 先看 schema，理解接口收什么、返回什么
2. 再看 security，理解密码和 token 如何处理
3. 再看 auth service，理解注册和登录业务逻辑
4. 最后看 route，理解 FastAPI 如何把这些层串起来
