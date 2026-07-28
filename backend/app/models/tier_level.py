import uuid
from enum import Enum as PyEnum

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TierName(str, PyEnum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"


class TierLevel(Base):
    __tablename__ = "tier_levels"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[TierName] = mapped_column(
        Enum(TierName),
        nullable=False,
        unique=True
    )