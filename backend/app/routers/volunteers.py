from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.volunteer import Volunteer

from app.schemas.volunteer import (
    VolunteerCreate,
    VolunteerResponse
)

from app.services.volunteer_service import create_volunteer


router = APIRouter(
    prefix="/volunteers",
    tags=["Volunteers"]
)


@router.post(
    "",
    response_model=VolunteerResponse
)
def register_volunteer(
    volunteer: VolunteerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_volunteer(
        db,
        current_user,
        volunteer
    )


@router.get(
    "/me",
    response_model=VolunteerResponse
)
def get_my_volunteer_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(Volunteer).filter(
        Volunteer.user_id == current_user.id
    ).first()