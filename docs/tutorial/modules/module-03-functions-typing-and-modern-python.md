# 模块 3：函数、类型提示与现代 Python 3.10+

## 学习目标

- 熟悉函数参数、返回值、作用域、闭包和生成器
- 能用 `type hints` 为代码补最基础的可读性
- 会使用 `X | Y`、`match-case`、`dataclass`

## 核心概念

- 类型提示默认不在运行时强制拦截错误
- `dataclass` 适合承载清晰的数据对象
- `match-case` 用于结构化分支，而不是替代所有 `if`

## 代码分析

本模块的示例在 `examples/module_03_typing/`。

- `task_types.py` 展示 dataclass、类型提示和业务函数
- `test_task_types.py` 用测试固定行为

重点观察：

- 为什么类型提示能提升重构安全感
- 为什么 dataclass 比字典更适合表达稳定结构
- `match-case` 在状态分支里比多层 if 更清晰的场景

## 与前端对照

- 类型提示与 TypeScript 相似，但它更偏“文档 + 静态分析辅助”
- dataclass 接近“带默认值和方法的数据对象”
- 生成器可以类比“惰性产出”的 iterable 管道

## 常用库与工具

- `dataclasses`
- `typing`
- `mypy`

## 实战任务

- 为任务状态流转写一个 dataclass
- 用 `match-case` 处理状态文案映射
- 补一个边界测试，确认非法状态会抛错

## 验证命令

```powershell
uv run pytest examples/module_03_typing -q
```
