import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import UserRole


class UserPublic(BaseModel):
    """Safe-to-expose user representation. Never includes hashed_password."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    full_name: str
    phone_number: str | None = None
    role: UserRole
    is_active: bool
    dzongkhag: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    skills: str | None = None
    created_at: datetime


class UserUpdate(BaseModel):
    """Fields a user may edit on their own profile (Module 2)."""

    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    phone_number: str | None = Field(default=None, max_length=20)
    dzongkhag: str | None = Field(default=None, max_length=100)
    bio: str | None = Field(default=None, max_length=1000)
    avatar_url: str | None = Field(default=None, max_length=500)
    skills: str | None = Field(default=None, max_length=500)


class AdminUserUpdate(UserUpdate):
    """Additional fields only an admin may change."""

    role: UserRole | None = None
    is_active: bool | None = None
