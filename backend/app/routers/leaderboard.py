from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.point_repository import PointRepository
from app.repositories.user_repository import UserRepository
from app.schemas.leaderboard import LeaderboardEntry
from app.services.leaderboard_service import LeaderboardScope, LeaderboardService

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


def get_leaderboard_service(db: AsyncSession = Depends(get_db)) -> LeaderboardService:
    return LeaderboardService(PointRepository(db), UserRepository(db))


@router.get("", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    scope: LeaderboardScope = Query(default=LeaderboardScope.ALL_TIME),
    limit: int = Query(default=50, ge=1, le=200),
    service: LeaderboardService = Depends(get_leaderboard_service),
):
    return await service.get_leaderboard(scope=scope, limit=limit)
