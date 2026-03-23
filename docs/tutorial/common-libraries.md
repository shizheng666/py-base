# 常用 Python 开发库说明

这份文档集中回答一个问题：你在学习 Python 全栈时，经常看到的库到底是干什么的、一般怎么 import、在项目里通常落在哪一层。

## 1. `venv`

### 这个库/工具干嘛的

`venv` 是 Python 标准库自带的虚拟环境工具，用来给每个项目创建一套独立依赖环境，避免全局安装的包互相污染。

### 常见使用方式

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 前端类比

可以把它理解为“给这个项目单独圈出一个 Python 运行环境”，作用接近项目本地依赖隔离。

## 2. `pip`

### 这个工具干嘛的

`pip` 是 Python 最常见的包安装工具，用来安装、升级、卸载第三方库。

### 常见使用方式

```powershell
pip install fastapi sqlalchemy pytest
```

### 什么时候用

- 安装学习阶段需要的库
- 结合 `requirements.txt` 管理传统项目依赖

## 3. `pytest`

### 这个库干嘛的

`pytest` 是 Python 生态最常用的测试框架，用来写单元测试、接口测试和参数化测试。

### 常见 import

```python
import pytest
```

### 这个 import 干嘛的

- `import pytest` 把 pytest 模块引入当前文件
- 然后你可以使用 `pytest.raises`、`pytest.mark.parametrize` 等能力

### 常见使用方式

```python
import pytest


def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("b cannot be 0")
    return a / b


def test_divide_rejects_zero() -> None:
    with pytest.raises(ValueError):
        divide(10, 0)
```

## 4. `ruff`

### 这个库干嘛的

`ruff` 是高性能的 lint 和代码质量工具，能帮你发现未使用导入、命名问题、部分风格问题。

### 常见使用方式

```powershell
uv run ruff check .
```

### 前端类比

非常接近 `ESLint`。

## 5. `mypy`

### 这个库干嘛的

`mypy` 是 Python 的静态类型检查工具。Python 的类型提示本身不会自动阻止程序运行，但 `mypy` 会在你执行检查时帮你发现很多潜在问题。

### 常见使用方式

```powershell
uv run mypy .
```

### 前端类比

像是给 Python 项目加上一层“更接近 TypeScript 审查体验”的检查流程。

## 6. `FastAPI`

### 这个库干嘛的

`FastAPI` 是一个现代 Python Web 框架，擅长构建 API，具备类型提示友好、自动生成 OpenAPI 文档、依赖注入清晰等特点。

### 常见 import

```python
from fastapi import FastAPI, APIRouter, Depends, status
```

### 这些 from/import 干嘛的

- `from fastapi import FastAPI`
  - 从 `fastapi` 这个库里取出 `FastAPI` 类
  - 它用来创建应用实例，比如 `app = FastAPI()`
- `from fastapi import APIRouter`
  - 用来组织一组路由，避免所有接口都堆在一个文件里
- `from fastapi import Depends`
  - 用来声明依赖注入，比如数据库会话、当前用户、配置对象
- `from fastapi import status`
  - 提供 HTTP 状态码常量，例如 `status.HTTP_201_CREATED`

### 常见使用方式

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
```

## 7. `Uvicorn`

### 这个库干嘛的

`Uvicorn` 是 ASGI 服务器，用来真正运行 FastAPI 应用。

### 常见使用方式

```powershell
uv run uvicorn projects.task_collab_api.app.main:app --reload
```

### 这个命令什么意思

- `projects.task_collab_api.app.main`：模块路径
- `:app`：模块里的应用实例变量名
- `--reload`：开发环境下代码变更后自动重启

## 8. `Pydantic`

### 这个库干嘛的

`Pydantic` 用来定义输入输出模型、做数据校验、做类型转换和序列化。

### 常见 import

```python
from pydantic import BaseModel, Field
```

### 这些 from/import 干嘛的

- `BaseModel`
  - 所有 Pydantic 模型的基类
  - 继承它之后，字段就会有校验和序列化能力
- `Field`
  - 给字段补充约束和说明
  - 比如最小长度、默认值、文档描述

### 常见使用方式

```python
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    priority: int = Field(default=3, ge=1, le=5)
```

## 9. `SQLAlchemy 2.x`

### 这个库干嘛的

`SQLAlchemy` 是 Python 后端里最常见的数据库访问库之一，既能写 ORM，也能写更底层的 SQL 表达式。

### 常见 import

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
```

### 这些 from/import 干嘛的

- `create_engine`
  - 创建数据库连接引擎
- `select`
  - 构造查询表达式
- `Session`
  - 数据库会话对象，负责查询、提交、回滚
- `DeclarativeBase`
  - ORM 模型基类
- `Mapped`
  - 给 ORM 字段做类型标注
- `mapped_column`
  - 声明 ORM 字段

### 常见使用方式

```python
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
```

## 10. `Alembic`

### 这个库干嘛的

`Alembic` 是数据库迁移工具，用来记录和执行表结构变更。学习后端时很重要，因为数据库不会像内存对象那样“改完就算了”，你需要可追踪的演进记录。

### 常见使用方式

```powershell
alembic revision --autogenerate -m "create tasks table"
alembic upgrade head
```

## 11. `psycopg`

### 这个库干嘛的

`psycopg` 是 PostgreSQL 驱动。SQLAlchemy 负责 ORM 和查询抽象，真正跟 PostgreSQL 说话时通常还需要具体驱动。

### 什么时候用

- 切换到 PostgreSQL 时
- 生产环境常见

## 12. `httpx`

### 这个库干嘛的

`httpx` 是一个现代 HTTP 客户端库，常用于请求第三方 API，也常被 FastAPI 测试客户端间接使用。

### 常见 import

```python
import httpx
```

### 常见使用方式

```python
import httpx


def fetch_status(url: str) -> int:
    response = httpx.get(url, timeout=5.0)
    return response.status_code
```

## 13. `Redis`

### 这个库/服务干嘛的

Redis 是内存型数据存储，常用来做缓存、消息中间件、分布式锁、任务队列后端。

### 在本教程里怎么用

- 模块 11 里把它作为后台任务和缓存扩展点

## 14. `Celery`

### 这个库干嘛的

`Celery` 是 Python 生态常见的任务队列框架，适合处理邮件发送、通知、批处理、定时任务等“不要阻塞主接口”的工作。

### 它和 Redis 的关系

Celery 常把 Redis 当作 broker 或 backend 使用。

## 15. `Docker`

### 这个工具干嘛的

`Docker` 用来把应用和运行环境一起打包，方便在不同机器上稳定运行。

### 在本教程里怎么用

- 为主项目提供统一运行环境
- 为后续部署和团队协作打基础

## 怎么看懂 `from ... import ...`

很多前端开发者刚转 Python 时，会把这类语句看得很碎。其实可以按下面方式理解：

```python
from fastapi import FastAPI
```

- `fastapi`：库或模块名
- `FastAPI`：从这个库里取出的具体类、函数或对象

再比如：

```python
from sqlalchemy.orm import Session, mapped_column
```

- `sqlalchemy.orm`：SQLAlchemy 里专门处理 ORM 的子模块
- `Session`：数据库会话类
- `mapped_column`：定义 ORM 字段的工具函数

## 学习建议

看到 import 时，不要只记名字，建议顺手问自己 4 个问题：

1. 这个库是做什么的
2. 这个模块负责哪一层
3. 我引入的是类、函数还是常量
4. 它在我的代码里起的是“入口、工具、模型、还是边界校验”的作用
