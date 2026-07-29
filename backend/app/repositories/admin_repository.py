from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance
from app.models.badge import UserBadge
from app.models.enums import AttendanceStatus, EventStatus, UserRole
from app.models.event import Event
from app.models.event_registration import EventRegistration
from app.models.point_transaction import PointTransaction
from app.models.user import User


class AdminRepository:
    """
    Deliberately queries multiple tables directly rather than going through
    each domain repository — the dashboard is a cross-cutting read model,
    not a write path, so this is the one place bypassing per-entity
    repositories is the cleaner choice.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _count(self, query) -> int:
        result = await self.db.execute(query)
        return int(result.scalar_one())

    async def count_users_by_role(self, role: UserRole | None = None) -> int:
        query = select(func.count()).select_from(User)
        if role:
            query = query.where(User.role == role)
        return await self._count(query)

    async def count_events(self, status: EventStatus | None = None, upcoming_only: bool = False) -> int:
        query = select(func.count()).select_from(Event)
        if status:
            query = query.where(Event.status == status)
        if upcoming_only:
            query = query.where(Event.start_datetime >= func.now())
        return await self._count(query)

    async def count_registrations(self) -> int:
        return await self._count(select(func.count()).select_from(EventRegistration))

    async def count_attendance_present(self) -> int:
        return await self._count(
            select(func.count())
            .select_from(Attendance)
            .where(Attendance.status == AttendanceStatus.PRESENT)
        )

    async def sum_points_awarded(self) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.sum(PointTransaction.amount), 0)).where(
                PointTransaction.amount > 0
            )
        )
        return int(result.scalar_one())

    async def count_badges_awarded(self) -> int:
        return await self._count(select(func.count()).select_from(UserBadge))
