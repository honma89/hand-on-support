from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.recognition import Recognition

from app.schemas.recognition import RecognitionCreate, RecognitionResponse

router = APIRouter(
    prefix="/recognitions",
    tags=["Recognitions"]
)


@router.get("", response_model=list[RecognitionResponse])
def list_recognitions(
    year: int | None = None,
    month: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Recognition)

    if year:
        query = query.filter(Recognition.year == year)

    if month:
        query = query.filter(Recognition.month == month)

    return query.order_by(
        Recognition.year.desc(), Recognition.month.desc()
    ).all()


@router.post("", response_model=RecognitionResponse)
def create_recognition(
    recognition: RecognitionCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    new_recognition = Recognition(**recognition.model_dump())

    db.add(new_recognition)
    db.commit()
    db.refresh(new_recognition)

    return new_recognition
