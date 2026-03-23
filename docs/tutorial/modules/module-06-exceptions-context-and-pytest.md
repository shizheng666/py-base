# 模块 6：异常处理、上下文管理与 pytest

## 学习目标

- 理解异常传播和自定义异常
- 看懂 `with` 和上下文管理器的价值
- 用 pytest 组织更像工程而不是演示脚本的测试

## 核心概念

- 异常不是“报错后再补 if”的替代品，而是业务边界的一部分
- `with` 常用于文件、数据库连接、锁和事务
- pytest 的价值在于可重复验证，不在于“比 unittest 语法短”

## 代码分析

本模块的示例在 `examples/module_06_validation/`。

- `validators.py` 包含输入校验和自定义异常
- `test_validators.py` 展示参数化测试和异常断言

重点观察：

- 为什么校验函数应该返回清晰的数据结构
- 什么时候抛异常比返回布尔值更合适
- 为什么测试名称要体现业务语义

## 与前端对照

- 类似前端中的表单校验、API 错误处理和 try/catch
- 但 Python 更强调显式异常类型和同步控制流的可读性

## 常用库

- `pytest`
- `contextlib`

## 实战任务

- 为任务标题、优先级、截止日期写校验函数
- 给非法输入写参数化测试
- 让错误信息能直接被 API 层消费

## 验证命令

```powershell
uv run pytest examples/module_06_validation -q
```
