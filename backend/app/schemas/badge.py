import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import BadgeCriteriaType


class BadgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str
    icon: str
    criteria_type: BadgeCriteriaType
    criteria_value: int


class UserBadgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    badge_id: uuid.UUID
    awarded_at: datetime
    badge: BadgeResponse
