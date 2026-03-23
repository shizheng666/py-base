# 模块 7：包管理、代码质量与项目结构

## 学习目标

- 理解 `requirements.txt`、`pyproject.toml`、工具配置的关系
- 学会组织目录，而不是把所有逻辑写进单文件
- 认识 lint、format、type check 在团队协作里的作用

## 核心概念

- `pyproject.toml` 是现代 Python 工程的重要入口
- `ruff` 负责快速静态检查和部分格式化能力
- `mypy` 帮你在大型重构前发现类型层面的风险

## 与前端对照

- `pyproject.toml` 有点像 `package.json + tsconfig + tool config` 的组合入口
- `ruff` 类似 `eslint + 部分格式化`
- `mypy` 接近“给 Python 项目补一层 TypeScript 式的检查”

## 主项目应用

本章开始把之前的脚本与小例子，升级成 `projects/task_collab_api/` 里的多模块结构：

- `api/`：HTTP 路由
- `schemas/`：输入输出模型
- `services/`：业务逻辑
- `models/`：数据库模型
- `db/`：数据库连接和会话

## 实战任务

- 解释主项目每个目录的职责
- 为新增功能先列文件边界，再开始写代码
- 运行一次 lint 和测试
