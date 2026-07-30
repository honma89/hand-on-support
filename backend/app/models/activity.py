import uuid

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Activity(Base):
    """A loggable type of volunteer work, independent of any specific event
    (e.g. remote design work, admin tasks) — default point/hour values act
    as suggestions when someone logs it."""

    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    default_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    default_hours: Mapped[float] = mapped_column(Numeric, default=0, nullable=False)

    activity_category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("activity_categories.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    activity_category: Mapped["ActivityCategory"] = relationship()

    def __repr__(self) -> str:
        return f"<Activity {self.name}>"
