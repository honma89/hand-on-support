from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.volunteer import Volunteer
from app.schemas.volunteer import VolunteerCreate
from app.models.user import User


def create_volunteer(
    db: Session,
    user: User,
    volunteer_data: VolunteerCreate
):
    existing = db.query(Volunteer).filter(
        Volunteer.user_id == user.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="A volunteer profile already exists for this user"
        )

    volunteer = Volunteer(
        user_id=user.id,
        firstname=volunteer_data.firstname,
        lastname=volunteer_data.lastname,
        date_of_birth=volunteer_data.date_of_birth,
        gender=volunteer_data.gender,
        phone_number=volunteer_data.phone_number,
        telegram_username=volunteer_data.telegram_username
    )

    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)

    return volunteer