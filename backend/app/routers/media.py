from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.media import Media

from app.schemas.media import MediaCreate, MediaResponse

router = APIRouter(
    prefix="/media",
    tags=["Media"]
)


@router.get("", response_model=list[MediaResponse])
def list_media(db: Session = Depends(get_db)):
    return db.query(Media).order_by(Media.created_at.desc()).all()


@router.post("", response_model=MediaResponse)
def create_media(
    media: MediaCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    new_media = Media(
        **media.model_dump(),
        uploaded_by=current_admin.id
    )

    db.add(new_media)
    db.commit()
    db.refresh(new_media)

    return new_media
