import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance
from app.models.enums import AttendanceStatus
from app.models.event import Event


class AttendanceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_event_and_user(self, event_id: uuid.UUID, user_id: uuid.UUID) -> Attendance | None:
        result = await self.db.execute(
            select(Attendance).where(Attendance.event_id == event_id, Attendance.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, attendance: Attendance) -> Attendance:
        self.db.add(attendance)
        await self.db.flush()
        await self.db.refresh(attendance)
        return attendance

    async def save(self, attendance: Attendance) -> Attendance:
        await self.db.flush()
        await self.db.refresh(attendance)
        return attendance

    async def list_for_event(self, event_id: uuid.UUID) -> list[Attendance]:
        result = await self.db.execute(
            select(Attendance).where(Attendance.event_id == event_id).order_by(Attendance.marked_at.asc())
        )
        return list(result.scalars().all())

    async def list_for_user(self, user_id: uuid.UUID) -> list[Attendance]:
        result = await self.db.execute(
            select(Attendance).where(Attendance.user_id == user_id).order_by(Attendance.marked_at.desc())
        )
        return list(result.scalars().all())

    async def count_present_for_user(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(Attendance).where(
                Attendance.user_id == user_id,
                Attendance.status == AttendanceStatus.PRESENT,
            )
        )
        return int(result.scalar_one())

    @staticmethod
    def _hours_query():
        """Sum of event duration (in seconds) for PRESENT attendance rows,
        via extract(epoch from interval) - callers convert to hours."""
        return (
            select(func.coalesce(func.sum(func.extract("epoch", Event.end_datetime - Event.start_datetime)), 0))
            .select_from(Attendance)
            .join(Event, Event.id == Attendance.event_id)
            .where(Attendance.status == AttendanceStatus.PRESENT)
        )

    async def sum_hours_for_user(self, user_id: uuid.UUID) -> float:
        query = self._hours_query().where(Attendance.user_id == user_id)
        result = await self.db.execute(query)
        return round(float(result.scalar_one()) / 3600, 1)

    async def sum_hours_all(self) -> float:
        result = await self.db.execute(self._hours_query())
        return round(float(result.scalar_one()) / 3600, 1)
