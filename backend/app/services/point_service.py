from sqlalchemy.orm import Session

from app.models.volunteer import Volunteer
from app.services.badge_service import check_and_award_badges


def award_points_and_hours(
    db: Session,
    volunteer: Volunteer,
    points: int,
    hours: float
):
    volunteer.points_total += points
    volunteer.hours_total = float(volunteer.hours_total) + hours

    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)

    check_and_award_badges(db, volunteer)

    return volunteer
