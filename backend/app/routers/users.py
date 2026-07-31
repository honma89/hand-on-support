import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.db.session import get_db
from app.deps import CurrentUser, get_user_repository, require_admin
from app.repositories.address_repository import AddressRepository
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.badge_repository import BadgeRepository
from app.repositories.point_repository import PointRepository
from app.repositories.user_repository import UserRepository
from app.schemas.impact import MyImpact
from app.schemas.location import AddressPublic, AddressUpdate
from app.schemas.user import AdminUserUpdate, UserPublic, UserUpdate
from app.services.address_service import AddressService
from app.services.impact_service import ImpactService
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
async def get_my_profile(current_user: CurrentUser):
    return current_user


@router.put("/me", response_model=UserPublic)
async def update_my_profile(
    data: UserUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    user_repo: UserRepository = Depends(get_user_repository),
):
    service = UserService(user_repo)
    updated = await service.update_own_profile(current_user, data)
    await db.commit()
    return updated


# NEW: there was previously no way at all to set a volunteer's structured
# Bhutan address (dzongkhag/gewog) in the live app - the addresses
# table existed in the DB but nothing wrote to it. User.dzongkhag (a plain
# string) is still used for quick filtering/display; this is the detailed,
# normalized version used for precise location lookups.
@router.put("/me/address", response_model=AddressPublic)
async def update_my_address(
    data: AddressUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    service = AddressService(AddressRepository(db))
    address = await service.set_user_address(current_user, data)
    await db.commit()
    return address


@router.get("/me/impact", response_model=MyImpact)
async def get_my_impact(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """One-call summary for a volunteer's own profile/dashboard: events
    attended, hours volunteered, point balance, badges earned, and current
    all-time leaderboard rank."""
    service = ImpactService(
        attendance_repo=AttendanceRepository(db),
        point_repo=PointRepository(db),
        badge_repo=BadgeRepository(db),
    )
    return await service.get_my_impact(current_user.id)


@router.get("/{user_id}", response_model=UserPublic)
async def get_user_public_profile(
    user_id: uuid.UUID,
    user_repo: UserRepository = Depends(get_user_repository),
):
    """Public volunteer profile — visible to any authenticated caller in future,
    kept open here since it exposes no sensitive fields."""
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


@router.get("", response_model=list[UserPublic], dependencies=[Depends(require_admin)])
async def list_users(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    user_repo: UserRepository = Depends(get_user_repository),
):
    service = UserService(user_repo)
    return await service.list_users(offset=offset, limit=limit)


@router.put("/{user_id}", response_model=UserPublic, dependencies=[Depends(require_admin)])
async def admin_update_user(
    user_id: uuid.UUID,
    data: AdminUserUpdate,
    db: AsyncSession = Depends(get_db),
    user_repo: UserRepository = Depends(get_user_repository),
):
    service = UserService(user_repo)
    try:
        updated = await service.admin_update_user(user_id, data)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    await db.commit()
    return updated
