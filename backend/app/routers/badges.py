import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps import CurrentUser, require_admin
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.badge_repository import BadgeRepository
from app.repositories.point_repository import PointRepository
from app.schemas.badge import BadgeCreate, BadgePublic, UserBadgePublic
from app.services.badge_service import BadgeService

router = APIRouter(prefix="/badges", tags=["badges"])


def get_badge_service(db: AsyncSession = Depends(get_db)) -> BadgeService:
    return BadgeService(BadgeRepository(db), AttendanceRepository(db), PointRepository(db))


@router.get("", response_model=list[BadgePublic])
async def list_badges(service: BadgeService = Depends(get_badge_service)):
    return await service.list_badges()


@router.get("/me", response_model=list[UserBadgePublic])
async def list_my_badges(
    current_user: CurrentUser,
    service: BadgeService = Depends(get_badge_service),
):
    return await service.list_user_badges(current_user.id)


@router.get("/users/{user_id}", response_model=list[UserBadgePublic])
async def list_user_badges(
    user_id: uuid.UUID,
    service: BadgeService = Depends(get_badge_service),
):
    return await service.list_user_badges(user_id)


@router.post(
    "",
    response_model=BadgePublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_badge(
    data: BadgeCreate,
    db: AsyncSession = Depends(get_db),
    service: BadgeService = Depends(get_badge_service),
):
    badge = await service.create_badge(data)
    await db.commit()
    return badge
