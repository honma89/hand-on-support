import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.dungkhag import Dungkhag
from app.models.dzongkhag import Dzongkhag
from app.models.gewog import Gewog
from app.schemas.location import DungkhagResponse, DzongkhagResponse, GewogResponse

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/dzongkhags", response_model=list[DzongkhagResponse])
async def list_dzongkhags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dzongkhag).order_by(Dzongkhag.name))
    return result.scalars().all()


@router.get("/dzongkhags/{dzongkhag_id}/dungkhags", response_model=list[DungkhagResponse])
async def list_dungkhags(dzongkhag_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Dungkhag).where(Dungkhag.dzongkhag_id == dzongkhag_id).order_by(Dungkhag.name)
    )
    return result.scalars().all()


@router.get("/dungkhags/{dungkhag_id}/gewogs", response_model=list[GewogResponse])
async def list_gewogs(dungkhag_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Gewog).where(Gewog.dungkhag_id == dungkhag_id).order_by(Gewog.name)
    )
    return result.scalars().all()
