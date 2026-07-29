from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance
from app.models.enums import AttendanceStatus, UserRole
from app.models.event import Event
from app.models.event_registration import EventRegistration
from app.models.point_transaction import PointTransaction
from app.models.user import User


class AnalyticsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def events_by_category(self) -> list[tuple[str, int]]:
        result = await self.db.execute(
            select(Event.category, func.count()).group_by(Event.category).order_by(func.count().desc())
        )
        return [(row[0], row[1]) for row in result.all()]

    async def volunteer_growth_by_month(self) -> list[tuple[object, int]]:
        month = func.date_trunc("month", User.created_at).label("month")
        result = await self.db.execute(
            select(month, func.count())
            .where(User.role == UserRole.VOLUNTEER)
            .group_by(month)
            .order_by(month.asc())
        )
        return [(row[0], row[1]) for row in result.all()]

    async def points_by_dzongkhag(self) -> list[tuple[str, int]]:
        result = await self.db.execute(
            select(User.dzongkhag, func.coalesce(func.sum(PointTransaction.amount), 0))
            .join(PointTransaction, PointTransaction.user_id == User.id)
            .where(User.dzongkhag.is_not(None))
            .group_by(User.dzongkhag)
            .order_by(func.sum(PointTransaction.amount).desc())
        )
        return [(row[0], int(row[1])) for row in result.all()]

    async def attendance_rate(self) -> tuple[int, int, int]:
        total_registrations_result = await self.db.execute(
            select(func.count()).select_from(EventRegistration)
        )
        total_registrations = int(total_registrations_result.scalar_one())

        present_result = await self.db.execute(
            select(func.count()).select_from(Attendance).where(Attendance.status == AttendanceStatus.PRESENT)
        )
        total_present = int(present_result.scalar_one())

        absent_result = await self.db.execute(
            select(func.count()).select_from(Attendance).where(Attendance.status == AttendanceStatus.ABSENT)
        )
        total_absent = int(absent_result.scalar_one())

        return total_registrations, total_present, total_absent
