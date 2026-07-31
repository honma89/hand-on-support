from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.admin_repository import AdminRepository
from app.repositories.announcement_repository import AnnouncementRepository
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.event_repository import EventRepository
from app.repositories.point_repository import PointRepository
from app.repositories.user_repository import UserRepository
from app.schemas.home import HomeResponse
from app.services.home_service import HomeService
from app.services.leaderboard_service import LeaderboardService

router = APIRouter(prefix="/home", tags=["home"])


def get_home_service(db: AsyncSession = Depends(get_db)) -> HomeService:
    return HomeService(
        event_repo=EventRepository(db),
        announcement_repo=AnnouncementRepository(db),
        admin_repo=AdminRepository(db),
        attendance_repo=AttendanceRepository(db),
        leaderboard_service=LeaderboardService(PointRepository(db), UserRepository(db)),
    )


@router.get("", response_model=HomeResponse)
async def get_home(service: HomeService = Depends(get_home_service)):
    """Public landing-page bundle: next 5 upcoming published events, latest
    5 announcements, top-5 all-time leaderboard, and site-wide impact
    stats - one call instead of four separate ones from the frontend."""
    return await service.get_home()
