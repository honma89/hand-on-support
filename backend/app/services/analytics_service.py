from app.repositories.analytics_repository import AnalyticsRepository
from app.schemas.analytics import AttendanceRate, CategoryCount, DzongkhagPoints, MonthlyGrowth


class AnalyticsService:
    def __init__(self, analytics_repo: AnalyticsRepository):
        self.analytics_repo = analytics_repo

    async def get_events_by_category(self) -> list[CategoryCount]:
        rows = await self.analytics_repo.events_by_category()
        return [CategoryCount(category=category, count=count) for category, count in rows]

    async def get_volunteer_growth(self) -> list[MonthlyGrowth]:
        rows = await self.analytics_repo.volunteer_growth_by_month()
        return [MonthlyGrowth(month=month, new_volunteers=count) for month, count in rows]

    async def get_points_by_dzongkhag(self) -> list[DzongkhagPoints]:
        rows = await self.analytics_repo.points_by_dzongkhag()
        return [DzongkhagPoints(dzongkhag=dzongkhag, total_points=total) for dzongkhag, total in rows]

    async def get_attendance_rate(self) -> AttendanceRate:
        total_registrations, total_present, total_absent = await self.analytics_repo.attendance_rate()
        marked = total_present + total_absent
        rate = (total_present / marked * 100) if marked > 0 else 0.0
        return AttendanceRate(
            total_registrations=total_registrations,
            total_present=total_present,
            total_absent=total_absent,
            attendance_rate_percent=round(rate, 1),
        )
