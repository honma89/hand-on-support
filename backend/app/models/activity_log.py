import uuid
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
    DateTime
)

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    activity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activities.id"),
        nullable=False
    )

    event_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("events.id"),
        nullable=True
    )

    points_earned: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    hours_logged: Mapped[float] = mapped_column(
        Numeric,
        default=0
    )

    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )