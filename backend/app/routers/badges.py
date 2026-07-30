from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps import CurrentUser, require_admin
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.badge_repository import BadgeRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.point_repository import PointRepository
from app.schemas.badge import BadgeCreate, BadgeResponse, UserBadgeResponse
from app.services.badge_service import BadgeService
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/badges", tags=["badges"])


def get_badge_service(db: AsyncSession = Depends(get_db)) -> BadgeService:
    return BadgeService(
        BadgeRepository(db),
        AttendanceRepository(db),
        PointRepository(db),
        NotificationService(NotificationRepository(db)),
    )


@router.get("", response_model=list[BadgeResponse])
async def list_badges(service: BadgeService = Depends(get_badge_service)):
    return await service.list_all()


@router.get("/me", response_model=list[UserBadgeResponse])
async def my_badges(
    current_user: CurrentUser,
    service: BadgeService = Depends(get_badge_service),
):
    return await service.list_for_user(current_user.id)


@router.post(
    "",
    response_model=BadgeResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_badge(
    data: BadgeCreate,
    db: AsyncSession = Depends(get_db),
    service: BadgeService = Depends(get_badge_service),
):
    badge = await service.create_badge(
        name=data.name,
        description=data.description,
        icon=data.icon,
        criteria_type=data.criteria_type,
        criteria_value=data.criteria_value,
    )
    await db.commit()
    return badge
