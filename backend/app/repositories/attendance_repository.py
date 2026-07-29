import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance
from app.models.enums import AttendanceStatus


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
