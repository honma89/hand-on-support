import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin
from app.db.session import Base
from app.models.enums import BadgeCriteriaType


class Badge(Base, TimestampMixin):
    __tablename__ = "badges"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    icon: Mapped[str] = mapped_column(String(10), nullable=False, default="🏅")  # emoji or short code

    criteria_type: Mapped[BadgeCriteriaType] = mapped_column(
        Enum(BadgeCriteriaType, name="badge_criteria_type"), nullable=False
    )
    criteria_value: Mapped[int] = mapped_column(Integer, nullable=False)

    user_badges: Mapped[list["UserBadge"]] = relationship(
        back_populates="badge", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Badge {self.name} ({self.criteria_type}>={self.criteria_value})>"


class UserBadge(Base):
    __tablename__ = "user_badges"
    __table_args__ = (UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    badge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("badges.id", ondelete="CASCADE"), nullable=False, index=True
    )
    awarded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="badges")
    badge: Mapped["Badge"] = relationship(back_populates="user_badges")

    def __repr__(self) -> str:
        return f"<UserBadge user={self.user_id} badge={self.badge_id}>"
