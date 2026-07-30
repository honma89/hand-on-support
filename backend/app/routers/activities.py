from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.models.activity import Activity
from app.models.activity_category import ActivityCategory
from app.models.activity_log import ActivityLog

from app.schemas.activity import (
    ActivityCategoryResponse,
    ActivityResponse,
    ActivityLogCreate,
    ActivityLogResponse
)

from app.services.activity_service import log_activity, approve_activity_log

router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


@router.get("/categories", response_model=list[ActivityCategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.query(ActivityCategory).order_by(ActivityCategory.name).all()


@router.get("", response_model=list[ActivityResponse])
def list_activities(
    category_id: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Activity)

    if category_id:
        query = query.filter(Activity.activity_category_id == category_id)

    return query.order_by(Activity.name).all()


@router.post("/logs", response_model=ActivityLogResponse)
def log_activity_endpoint(
    log_data: ActivityLogCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return log_activity(db, log_data)


@router.get("/logs/me", response_model=list[ActivityLogResponse])
def my_activity_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(ActivityLog).filter(
        ActivityLog.user_id == current_user.id
    ).order_by(ActivityLog.created_at.desc()).all()


@router.get("/logs/pending", response_model=list[ActivityLogResponse])
def pending_activity_logs(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return db.query(ActivityLog).filter(
        ActivityLog.approved_at.is_(None)
    ).order_by(ActivityLog.created_at).all()


@router.post("/logs/{log_id}/approve", response_model=ActivityLogResponse)
def approve_activity_log_endpoint(
    log_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    log = db.query(ActivityLog).filter(ActivityLog.id == log_id).first()

    if not log:
        raise HTTPException(status_code=404, detail="Activity log not found")

    if log.approved_at:
        raise HTTPException(status_code=400, detail="Already approved")

    return approve_activity_log(db, log, current_admin.id)
