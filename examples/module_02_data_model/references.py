"""Reference semantics example for module 2.

这个例子专门解释 Python 里的“名字绑定到对象”。
很多前端开发者第一次学 Python 时会觉得它和 JS 很像，
但一遇到可变对象共享引用，还是很容易踩坑。
"""

from __future__ import annotations


def clone_and_append(tags: list[str], new_tag: str) -> list[str]:
    """Return a new list instead of mutating the original list.

    这段代码展示的是“安全复制再修改”的做法：
    - `tags.copy()` 会创建一个浅拷贝列表
    - 后续 append 发生在新列表上
    - 原始列表保持不变

    这对于函数式风格、不可变思维、以及减少副作用很有帮助。
    """

    copied_tags = tags.copy()
    copied_tags.append(new_tag)
    return copied_tags

