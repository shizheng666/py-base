"""Default-argument example for module 2.

这个文件聚焦 Python 里最经典的坑之一：
`def func(items=[]): ...`
默认参数只在函数定义时求值一次，不是每次调用重新创建。
"""

from __future__ import annotations


def add_tag_safe(tag: str, tags: list[str] | None = None) -> list[str]:
    """Add a tag without leaking state across calls.

    为什么使用 `None`：
    - `None` 是一个明确的“没有传值”信号
    - 函数体内部再创建新列表，能保证每次调用拿到独立对象

    这是 Python 里非常常见、也非常重要的一种写法。
    """

    normalized_tags = [] if tags is None else tags.copy()
    normalized_tags.append(tag)
    return normalized_tags

