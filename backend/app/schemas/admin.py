import uuid

from pydantic import BaseModel

from app.models.user import UserStatus
from app.models.role import RoleName


class RoleAssign(BaseModel):
    user_id: uuid.UUID
    role: RoleName


class UserStatusUpdate(BaseModel):
    status: UserStatus


class TierAssign(BaseModel):
    tier_level_id: uuid.UUID
