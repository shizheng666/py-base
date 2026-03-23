# Python 3.10+ Full-Stack Roadmap for Frontend Developers

这是一套面向资深前端开发者的 Python 3.10+ 全栈学习教程。目标不是把 Python 语法零散背下来，而是帮你建立一条从 `JavaScript/TypeScript -> Python -> FastAPI -> 数据库 -> 异步任务 -> 部署` 的完整迁移路径。

## 你会得到什么

- 一套 12 个模块的系统教程，放在 `docs/tutorial/modules/`
- 一套统一的代码讲解规范，放在 `docs/tutorial/teaching-standards.md`
- 多个可运行示例，放在 `examples/`
- 一个渐进式主项目骨架 `任务/协作系统 API`，放在 `projects/task_collab_api/`

## 学习方式

建议按下面的节奏推进：

1. 先读模块文档，明确“这一章到底要解决什么问题”
2. 再跑对应示例，观察输入、输出和测试
3. 接着把知识点迁移到主项目里
4. 每章结束都做验证，不用“感觉会了”代替证据

## 教程结构

- `docs/tutorial/README.md`：课程地图和推荐节奏
- `docs/tutorial/teaching-standards.md`：代码设计、代码讲解和练习验证规范
- `docs/tutorial/modules/`：12 个学习模块
- `examples/`：独立的小型示例和测试
- `projects/task_collab_api/`：FastAPI 主项目

## 推荐环境

本仓库的教程以 `Python 3.10+` 为基线，建议优先使用 `uv` 管理 Python 与依赖，因为在没有系统 Python 的 Windows 环境里也更容易启动：

```powershell
uv python install 3.12
uv venv --python 3.12
uv sync
```

如果你更习惯官方方式，也可以使用 `venv + pip`。

## 学习产出

学完这套内容后，你应该能：

- 用 Python 写中小型模块、脚本和测试
- 理解 Python 与 JS/TS 的语义差异
- 使用 FastAPI、SQLAlchemy 2.x、Pydantic 构建 API
- 把数据库、异步任务、日志、测试和部署连成一条完整链路
- 用前端的 API 协作视角审视 Python 后端设计
