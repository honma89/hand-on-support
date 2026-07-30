import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Dungkhag(Base):
    """Sub-district within a dzongkhag."""

    __tablename__ = "dungkhags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    dzongkhag_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dzongkhags.id", ondelete="CASCADE"), nullable=False, index=True
    )
    dzongkhag: Mapped["Dzongkhag"] = relationship()

    def __repr__(self) -> str:
        return f"<Dungkhag {self.name}>"
