"""Minimal authentication example for module 10.

这个 example 不直接复刻主项目的 FastAPI 路由和数据库层，
而是专门讲“认证原理的最小版本”：
1. 注册用户并存储密码哈希
2. 登录时验证密码
3. 登录成功后签发 JWT
4. 解析 token 还原用户身份
"""

from __future__ import annotations

from dataclasses import dataclass  # `dataclass` 用来快速定义“以数据为主”的对象，这里适合表示一个学习用用户记录。
from datetime import UTC  # `UTC` 用于生成带时区的过期时间，让 token 时间信息更清晰。
from datetime import datetime  # `datetime` 用来记录注册时间和 token 过期时间。
from datetime import timedelta  # `timedelta` 用来表达“30 分钟后过期”这类时间偏移。
import hashlib  # `hashlib` 是标准库里的哈希工具，这里用来演示密码哈希的基础思路。
import hmac  # `hmac.compare_digest` 用于安全比较字符串，避免直接 `==` 带来的时序差异风险。
import secrets  # `secrets` 用来生成适合安全场景的随机盐。

import jwt  # `jwt` 来自 PyJWT，用于生成和解析 JSON Web Token。


DEMO_JWT_SECRET = "example-module-10-secret-key-at-least-32"
DEMO_JWT_ALGORITHM = "HS256"


class AuthenticationError(ValueError):
    """Raised when credentials or tokens are invalid."""


@dataclass(slots=True)
class DemoUser:
    """A minimal user record for learning authentication flows."""

    email: str
    full_name: str
    password_hash: str
    created_at: datetime


class SimpleUserStore:
    """A tiny in-memory user store.

    这里不用数据库，是为了把学习重点放在认证原理本身，
    避免一开始被 ORM、会话和路由层分散注意力。
    """

    def __init__(self) -> None:
        self._users_by_email: dict[str, DemoUser] = {}

    def save(self, user: DemoUser) -> None:
        self._users_by_email[user.email] = user

    def find_by_email(self, email: str) -> DemoUser | None:
        return self._users_by_email.get(email.strip().lower())


def hash_password_for_learning(password: str, salt: str | None = None) -> str:
    """Hash a password with a random salt.

    这是一个适合教学的基础版本：
    - 不保存明文密码
    - 每个密码都有自己的盐
    - 最终以 `salt$hash` 的形式存储
    """

    selected_salt = salt or secrets.token_hex(16)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        selected_salt.encode("utf-8"),
        100_000,
    )
    return f"{selected_salt}${derived_key.hex()}"


def verify_password_for_learning(password: str, stored_hash: str) -> bool:
    """Verify a plain password against the stored salt+hash string."""

    salt, expected_hash = stored_hash.split("$", maxsplit=1)
    recalculated_hash = hash_password_for_learning(password, salt).split("$", maxsplit=1)[1]
    return hmac.compare_digest(expected_hash, recalculated_hash)


def register_user(
    store: SimpleUserStore,
    *,
    email: str,
    password: str,
    full_name: str,
) -> DemoUser:
    """Register one user in the in-memory store."""

    normalized_email = email.strip().lower()

    if store.find_by_email(normalized_email) is not None:
        raise AuthenticationError("Email is already registered")

    user = DemoUser(
        email=normalized_email,
        full_name=full_name.strip(),
        password_hash=hash_password_for_learning(password),
        created_at=datetime.now(UTC),
    )
    store.save(user)
    return user


def create_token_for_learning(email: str, expires_in_minutes: int = 30) -> str:
    """Issue a short-lived JWT token for one user email."""

    payload = {
        "sub": email.strip().lower(),
        "exp": datetime.now(UTC) + timedelta(minutes=expires_in_minutes),
    }
    return jwt.encode(payload, DEMO_JWT_SECRET, algorithm=DEMO_JWT_ALGORITHM)


def decode_token_for_learning(token: str) -> dict:
    """Decode one JWT token and surface learning-friendly errors."""

    try:
        return jwt.decode(
            token,
            DEMO_JWT_SECRET,
            algorithms=[DEMO_JWT_ALGORITHM],
        )
    except jwt.PyJWTError as error:
        raise AuthenticationError("Invalid or expired token") from error


def login_user(
    store: SimpleUserStore,
    *,
    email: str,
    password: str,
) -> dict[str, str]:
    """Authenticate one user and return a token response.

    返回值故意模仿真实 API 常见结构：
    - `access_token`
    - `token_type`

    这样学习者稍后切换到主项目时，更容易把 example 和真实接口对应起来。
    """

    user = store.find_by_email(email)
    if user is None or not verify_password_for_learning(password, user.password_hash):
        raise AuthenticationError("Invalid email or password")

    return {
        "access_token": create_token_for_learning(user.email),
        "token_type": "bearer",
    }
