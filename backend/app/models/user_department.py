import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin
from app.db.session import Base


class UserDepartment(Base, TimestampMixin):
    """Join table: which department(s) a user belongs to, and their title there."""

    __tablename__ = "user_departments"
    __table_args__ = (UniqueConstraint("user_id", "department_id", name="uq_user_department"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role_title: Mapped[str | None] = mapped_column(String(100), nullable=True)

    user: Mapped["User"] = relationship(foreign_keys=[user_id])
    department: Mapped["Department"] = relationship()

    def __repr__(self) -> str:
        return f"<UserDepartment user={self.user_id} department={self.department_id}>"
