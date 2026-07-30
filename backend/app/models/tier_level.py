from enum import StrEnum
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class TierName(StrEnum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


class TierLevel(Base):
    """Lookup table of volunteer recognition tiers, keyed off lifetime points."""

    __tablename__ = "tier_levels"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[TierName] = mapped_column(Enum(TierName, name="tier_name"), nullable=False, unique=True)
    min_points: Mapped[int | None] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<TierLevel {self.name}>"
