# 模块 5：标准库与常见工程能力

## 学习目标

- 熟练使用路径、时间、JSON、日志、枚举和 UUID
- 形成“先找标准库，再看第三方库”的思维
- 能写出更可靠的脚本和服务代码

## 核心概念

- `pathlib` 比字符串拼路径更安全
- `datetime` 是后端业务中高频但容易出错的领域
- `logging` 是可观测性的起点，不要只靠 `print`

## 建议重点掌握

- `pathlib.Path`
- `datetime`
- `json`
- `logging`
- `uuid`
- `enum`

## 与前端对照

- `pathlib` 类似 Node.js 里的 `path`
- `json` 与 JS 世界天然相近，但序列化边界仍要注意
- `logging` 接近后端版的结构化调试输出

## 实战任务

- 用 `pathlib` 写文件导出脚本
- 用 `logging` 记录脚本执行过程
- 用 `uuid` 给任务对象生成外部 ID
