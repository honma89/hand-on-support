from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.models.badge import Badge
from app.models.user_badge import UserBadge

from app.schemas.badge import BadgeResponse, UserBadgeResponse
from app.services.badge_service import award_badge_manually

router = APIRouter(
    prefix="/badges",
    tags=["Badges"]
)


@router.get("", response_model=list[BadgeResponse])
def list_badges(db: Session = Depends(get_db)):
    return db.query(Badge).order_by(Badge.points_required).all()


@router.get("/me", response_model=list[UserBadgeResponse])
def my_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(UserBadge).filter(
        UserBadge.user_id == current_user.id
    ).all()


@router.post("/{badge_id}/award/{user_id}", response_model=UserBadgeResponse)
def award_badge(
    badge_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    badge = db.query(Badge).filter(Badge.id == badge_id).first()

    if not badge:
        raise HTTPException(status_code=404, detail="Badge not found")

    return award_badge_manually(db, user_id, badge_id)
