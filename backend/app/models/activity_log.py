import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin
from app.db.session import Base


class ActivityLog(Base, TimestampMixin):
    """A user logging (self-reported, then admin-approved) time against an
    Activity — optionally tied to a specific Event. Separate from the
    Attendance/PointTransaction flow, which is event-check-in specific."""

    __tablename__ = "activity_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("activities.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("events.id", ondelete="SET NULL"), nullable=True
    )

    points_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hours_logged: Mapped[float] = mapped_column(Numeric, default=0, nullable=False)

    approved_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(foreign_keys=[user_id])
    activity: Mapped["Activity"] = relationship()
    event: Mapped["Event"] = relationship()
    approved_by: Mapped["User"] = relationship(foreign_keys=[approved_by_id])

    def __repr__(self) -> str:
        return f"<ActivityLog user={self.user_id} activity={self.activity_id}>"
