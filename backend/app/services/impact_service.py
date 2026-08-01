import uuid

from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.badge_repository import BadgeRepository
from app.repositories.point_repository import PointRepository
from app.schemas.impact import MyImpact


class ImpactService:
    def __init__(
        self,
        attendance_repo: AttendanceRepository,
        point_repo: PointRepository,
        badge_repo: BadgeRepository,
    ):
        self.attendance_repo = attendance_repo
        self.point_repo = point_repo
        self.badge_repo = badge_repo

    async def get_my_impact(self, user_id: uuid.UUID) -> MyImpact:
        return MyImpact(
            events_attended=await self.attendance_repo.count_present_for_user(user_id),
            hours_volunteered=await self.attendance_repo.sum_hours_for_user(user_id),
            total_points=await self.point_repo.get_balance(user_id),
            badges_earned=len(await self.badge_repo.list_earned_badge_ids(user_id)),
            leaderboard_rank=await self.point_repo.get_user_rank(user_id),
        )
