"""Pydantic schemas for authentication and user output."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class UserRegister(BaseModel):
    """Payload used to create a new user."""

    email: str = Field(min_length=5, max_length=255, description="Unique login email.")
    password: str = Field(min_length=8, max_length=255, description="Plain password before hashing.")
    full_name: str = Field(min_length=1, max_length=120, description="Display name for the user.")


class UserLogin(BaseModel):
    """Payload used to log a user in."""

    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=255)


class UserRead(BaseModel):
    """Public user profile returned by the API."""

    id: int
    email: str
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AccessToken(BaseModel):
    """Response body returned after successful login."""

    access_token: str
    token_type: str = "bearer"
