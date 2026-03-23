"""A tiny CLI example for module 1.

这个文件故意写得比“真实生产环境的最短写法”更啰嗦，
因为目标不是炫技，而是帮助前端开发者看清 Python CLI 程序的基本结构。
"""

from __future__ import annotations  # `annotations` 未来特性可以让类型提示延迟解析，写大型项目时更方便处理前向引用。

import sys  # `sys` 是标准库，用来读取命令行参数、退出码和解释器状态；CLI 程序几乎都会接触它。


def build_greeting(name: str) -> str:
    """Build a stable greeting message.

    为什么要单独提这个函数：
    1. 让核心逻辑可测试，而不是把逻辑全塞在 `print` 里。
    2. 让 CLI 层只负责接收输入和展示输出。
    3. 这就是后面写 API 时“路由层”和“业务层”拆分思路的最小版本。
    """

    cleaned_name = name.strip()
    return f"Hello, {cleaned_name}! Welcome to Python."


def main(argv: list[str] | None = None) -> int:
    """Run the CLI entry point.

    `argv` 代表命令行参数列表。
    - 如果外部没有传入，我们就从 `sys.argv` 读取真实的命令行参数。
    - `sys.argv[0]` 通常是脚本名，所以真正的业务参数从索引 1 开始。

    返回整数是一个常见 CLI 习惯：
    - `0` 表示成功
    - 非 0 表示失败
    """

    runtime_args = sys.argv[1:] if argv is None else argv

    if not runtime_args:
        print("Usage: python greet.py <name>")
        return 1

    print(build_greeting(runtime_args[0]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

