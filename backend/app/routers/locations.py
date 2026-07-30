from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.dzongkhag import Dzongkhag
from app.models.dungkhag import Dungkhag
from app.models.gewog import Gewog

from app.schemas.location import (
    DzongkhagResponse,
    DungkhagResponse,
    GewogResponse
)

router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)


@router.get("/dzongkhags", response_model=list[DzongkhagResponse])
def list_dzongkhags(db: Session = Depends(get_db)):
    return db.query(Dzongkhag).order_by(Dzongkhag.name).all()


@router.get(
    "/dzongkhags/{dzongkhag_id}/dungkhags",
    response_model=list[DungkhagResponse]
)
def list_dungkhags(dzongkhag_id: str, db: Session = Depends(get_db)):
    return db.query(Dungkhag).filter(
        Dungkhag.dzongkhag_id == dzongkhag_id
    ).order_by(Dungkhag.name).all()


@router.get(
    "/dungkhags/{dungkhag_id}/gewogs",
    response_model=list[GewogResponse]
)
def list_gewogs(dungkhag_id: str, db: Session = Depends(get_db)):
    return db.query(Gewog).filter(
        Gewog.dungkhag_id == dungkhag_id
    ).order_by(Gewog.name).all()
