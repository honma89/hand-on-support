import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class DocumentCategory(str, PyEnum):
    PROPOSAL = "PROPOSAL"
    REPORT = "REPORT"
    NOTICE = "NOTICE"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    category: Mapped[DocumentCategory] = mapped_column(
        Enum(DocumentCategory),
        nullable=False
    )

    file_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )