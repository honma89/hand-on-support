import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UserDepartment(Base):
    __tablename__ = "user_departments"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False
    )

    role_title: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )