import uuid
from enum import StrEnum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin
from app.db.session import Base


class DocumentCategory(StrEnum):
    PROPOSAL = "proposal"
    REPORT = "report"
    NOTICE = "notice"


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[DocumentCategory] = mapped_column(Enum(DocumentCategory, name="document_category"), nullable=False)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)

    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    uploaded_by: Mapped["User"] = relationship()

    def __repr__(self) -> str:
        return f"<Document {self.title} ({self.category})>"
