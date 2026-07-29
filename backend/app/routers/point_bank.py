import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationError
from app.db.session import get_db
from app.deps import CurrentUser, require_admin
from app.repositories.point_repository import PointRepository
from app.schemas.point_bank import (
    PointAdjustmentRequest,
    PointBalanceResponse,
    PointRedeemRequest,
    PointTransactionPublic,
)
from app.services.point_service import PointService

router = APIRouter(prefix="/points", tags=["point-bank"])


def get_point_service(db: AsyncSession = Depends(get_db)) -> PointService:
    return PointService(PointRepository(db))


@router.get("/me/balance", response_model=PointBalanceResponse)
async def get_my_balance(
    current_user: CurrentUser,
    service: PointService = Depends(get_point_service),
):
    balance = await service.get_balance(current_user.id)
    return PointBalanceResponse(user_id=current_user.id, balance=balance)


@router.get("/me/history", response_model=list[PointTransactionPublic])
async def get_my_history(
    current_user: CurrentUser,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    service: PointService = Depends(get_point_service),
):
    return await service.get_history(current_user.id, offset=offset, limit=limit)


@router.post("/me/redeem", response_model=PointTransactionPublic, status_code=status.HTTP_201_CREATED)
async def redeem_points(
    data: PointRedeemRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: PointService = Depends(get_point_service),
):
    try:
        transaction = await service.redeem_points(current_user.id, data.amount, data.description)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    await db.commit()
    return transaction


@router.get("/{user_id}/balance", response_model=PointBalanceResponse, dependencies=[Depends(require_admin)])
async def get_user_balance(
    user_id: uuid.UUID,
    service: PointService = Depends(get_point_service),
):
    balance = await service.get_balance(user_id)
    return PointBalanceResponse(user_id=user_id, balance=balance)


@router.post(
    "/adjust",
    response_model=PointTransactionPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def admin_adjust_points(
    data: PointAdjustmentRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    service: PointService = Depends(get_point_service),
):
    try:
        transaction = await service.adjust_points(
            data.user_id, data.amount, data.description, admin_id=current_user.id
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    await db.commit()
    return transaction
