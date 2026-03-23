"""Security helpers for password hashing and JWT tokens.

这里同时展示两类“安全相关代码”：
1. 密码不能明文存储，需要先做不可逆哈希
2. 登录成功后需要一个可验证的访问令牌，这里用 JWT
"""

from __future__ import annotations

from datetime import UTC  # 用来创建带时区的过期时间。
from datetime import datetime
from datetime import timedelta
import hashlib  # `hashlib` 是标准库里的哈希工具，这里用来派生密码哈希。
import hmac  # `hmac.compare_digest` 用于安全比较，避免直接字符串比较带来的时序风险。
import secrets  # `secrets` 适合生成安全随机值，这里用来生成密码盐。

import jwt  # `jwt` 来自 PyJWT，用于创建和验证 JSON Web Token。


ALGORITHM = "HS256"


def hash_password(password: str, salt: str | None = None) -> str:
    """Hash a plain password with PBKDF2.

    这里没有直接使用明文密码，而是：
    - 先生成随机盐
    - 再用 `pbkdf2_hmac` 做多轮派生
    - 最终把 `盐$哈希值` 存起来

    这是一种适合教学和小型项目理解的方案。
    """

    selected_salt = salt or secrets.token_hex(16)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        selected_salt.encode("utf-8"),
        100_000,
    )
    return f"{selected_salt}${derived_key.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Compare a plain password with a stored hash."""

    salt, current_hash = stored_hash.split("$", maxsplit=1)
    recalculated_hash = hash_password(password, salt).split("$", maxsplit=1)[1]
    return hmac.compare_digest(current_hash, recalculated_hash)


def create_access_token(
    *,
    subject: str,
    secret_key: str,
    expires_in_minutes: int = 60,
) -> str:
    """Create a signed JWT token.

    `subject` 通常是“这个令牌代表谁”，这里直接存用户邮箱，
    后面做更正式的系统时也可以改成用户 ID。
    """

    expires_at = datetime.now(UTC) + timedelta(minutes=expires_in_minutes)
    payload = {
        "sub": subject,
        "exp": expires_at,
    }
    return jwt.encode(payload, secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str, secret_key: str) -> dict:
    """Decode and validate one JWT token.

    如果令牌非法、过期、被篡改，PyJWT 会抛异常，
    调用方应该把它翻译成 401 Unauthorized。
    """

    return jwt.decode(token, secret_key, algorithms=[ALGORITHM])
