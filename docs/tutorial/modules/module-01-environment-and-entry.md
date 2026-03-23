# 模块 1：Python 开发环境与工程入口

## 学习目标

- 理解解释器、虚拟环境、模块、包和入口文件
- 能建立一个最小 Python 工程并运行测试
- 看懂 `__name__ == "__main__"` 的用途

## 核心概念

- 解释器：真正执行 `.py` 文件的程序
- 虚拟环境：隔离依赖版本，类似前端项目的局部 `node_modules`
- 模块：一个 `.py` 文件就是一个模块
- 包：包含 `__init__.py` 的目录
- 入口文件：程序启动点

## 代码分析

本模块的示例在 `examples/module_01_cli/`。

- `greet.py` 展示最小脚本、函数提取和 CLI 入口
- `test_greet.py` 演示如何用 pytest 验证行为

重点观察：

- 为什么把打印逻辑提取为可测试函数
- 为什么入口逻辑放在 `main()` 里更清晰
- 为什么脚本和可复用函数要分开

## 与前端对照

- `python greet.py Alice` 类似 `node greet.js Alice`
- 模块导入类似 ES Module，但 Python 的执行与导入时机更直接
- `venv` 的隔离作用接近于“每个项目单独一套依赖”

## 常用库与工具

- `venv`
- `pip`
- `pytest`
- `pathlib`

## 实战任务

- 跑通 `greet.py`
- 改造输出格式，比如加入时间或语言选项
- 为新增逻辑补测试

## 验证命令

```powershell
uv run pytest examples/module_01_cli -q
uv run python examples/module_01_cli/greet.py Alice
```
