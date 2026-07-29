from datetime import datetime, timedelta, timezone
from enum import StrEnum

from app.repositories.point_repository import PointRepository
from app.repositories.user_repository import UserRepository
from app.schemas.leaderboard import LeaderboardEntry


class LeaderboardScope(StrEnum):
    ALL_TIME = "all_time"
    MONTHLY = "monthly"
    WEEKLY = "weekly"


class LeaderboardService:
    def __init__(self, point_repo: PointRepository, user_repo: UserRepository):
        self.point_repo = point_repo
        self.user_repo = user_repo

    @staticmethod
    def _since_for_scope(scope: LeaderboardScope) -> datetime | None:
        now = datetime.now(timezone.utc)
        if scope == LeaderboardScope.MONTHLY:
            return now - timedelta(days=30)
        if scope == LeaderboardScope.WEEKLY:
            return now - timedelta(days=7)
        return None

    async def get_leaderboard(
        self, scope: LeaderboardScope = LeaderboardScope.ALL_TIME, limit: int = 50
    ) -> list[LeaderboardEntry]:
        since = self._since_for_scope(scope)
        ranked = await self.point_repo.get_leaderboard(since=since, limit=limit)

        entries: list[LeaderboardEntry] = []
        for rank, (user_id, total_points) in enumerate(ranked, start=1):
            user = await self.user_repo.get_by_id(user_id)
            if not user:
                continue
            entries.append(
                LeaderboardEntry(
                    rank=rank,
                    user_id=user.id,
                    full_name=user.full_name,
                    avatar_url=user.avatar_url,
                    dzongkhag=user.dzongkhag,
                    total_points=total_points,
                )
            )
        return entries
