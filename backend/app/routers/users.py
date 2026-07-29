import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.db.session import get_db
from app.deps import CurrentUser, get_user_repository, require_admin
from app.repositories.user_repository import UserRepository
from app.schemas.user import AdminUserUpdate, UserPublic, UserUpdate
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
