import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Gewog(Base):
    """Village block — smallest administrative unit, within a dungkhag."""

    __tablename__ = "gewogs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    dungkhag_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dungkhags.id", ondelete="CASCADE"), nullable=False, index=True
    )
    dungkhag: Mapped["Dungkhag"] = relationship()

    def __repr__(self) -> str:
        return f"<Gewog {self.name}>"
