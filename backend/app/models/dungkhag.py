import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Dungkhag(Base):
    __tablename__ = "dungkhags"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    dzongkhag_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dzongkhags.id"),
        nullable=False
    )