"""Pytest shared setup for the teaching examples.

这个文件不是业务代码，而是测试运行时的辅助配置。
它的作用是把每个示例目录加入 Python 的导入搜索路径，
这样测试文件就可以直接使用 `from greet import build_greeting`
这类更适合教学的导入方式。
"""

from pathlib import Path  # `Path` 来自标准库 `pathlib`，用面向对象的方式处理路径，比字符串拼接更安全。
import sys  # `sys` 来自标准库，用来访问解释器运行时信息，这里用它修改导入搜索路径 `sys.path`。


EXAMPLE_DIRS = [
    Path(__file__).parent / "module_01_cli",
    Path(__file__).parent / "module_02_data_model",
    Path(__file__).parent / "module_03_typing",
    Path(__file__).parent / "module_06_validation",
]

for directory in EXAMPLE_DIRS:
    directory_as_text = str(directory)
    if directory_as_text not in sys.path:
        sys.path.insert(0, directory_as_text)

