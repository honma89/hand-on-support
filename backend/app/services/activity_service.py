from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.activity_log import ActivityLog
from app.models.volunteer import Volunteer
from app.schemas.activity import ActivityLogCreate
from app.services.point_service import award_points_and_hours


def log_activity(db: Session, data: ActivityLogCreate):
    activity = db.query(Activity).filter(
        Activity.id == data.activity_id
    ).first()

    log = ActivityLog(
        user_id=data.user_id,
        activity_id=data.activity_id,
        event_id=data.event_id,
        points_earned=(
            data.points_earned
            if data.points_earned is not None
            else (activity.default_points if activity else 0)
        ),
        hours_logged=(
            data.hours_logged
            if data.hours_logged is not None
            else (activity.default_hours if activity else 0)
        )
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def approve_activity_log(db: Session, log: ActivityLog, approved_by):
    log.approved_by = approved_by
    log.approved_at = datetime.now(timezone.utc)

    db.add(log)
    db.commit()
    db.refresh(log)

    volunteer = db.query(Volunteer).filter(
        Volunteer.user_id == log.user_id
    ).first()

    if volunteer:
        award_points_and_hours(
            db,
            volunteer,
            log.points_earned,
            float(log.hours_logged)
        )

    return log
