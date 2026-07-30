import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import PointTransactionType


class PointBalanceResponse(BaseModel):
    user_id: uuid.UUID
    balance: int


class PointTransactionPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    event_id: uuid.UUID | None
    amount: int
    type: PointTransactionType
    description: str
    created_at: datetime


class PointAdjustmentRequest(BaseModel):
    """Admin-only manual correction — amount may be positive or negative."""

    user_id: uuid.UUID
    amount: int = Field(description="Positive to credit, negative to debit.")
    description: str = Field(min_length=3, max_length=300)


class PointRedeemRequest(BaseModel):
    amount: int = Field(gt=0)
    description: str = Field(min_length=3, max_length=300)
