import uuid
from datetime import datetime

from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str
    description: str | None = None
    head_user_id: uuid.UUID | None = None


class DepartmentResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    head_user_id: uuid.UUID | None
    created_at: datetime

    class Config:
        from_attributes = True


class DepartmentMemberAdd(BaseModel):
    user_id: uuid.UUID
    role_title: str | None = None


class DepartmentMemberResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    department_id: uuid.UUID
    role_title: str | None

    class Config:
        from_attributes = True
