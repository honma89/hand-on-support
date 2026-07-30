import uuid
from enum import StrEnum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin
from app.db.session import Base


class MediaType(StrEnum):
    PHOTO = "photo"
    VIDEO = "video"


class Media(Base, TimestampMixin):
    __tablename__ = "medias"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType, name="media_type"), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)

    event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("events.id", ondelete="SET NULL"), nullable=True
    )
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    event: Mapped["Event"] = relationship()
    uploaded_by: Mapped["User"] = relationship()

    def __repr__(self) -> str:
        return f"<Media {self.title} ({self.type})>"
