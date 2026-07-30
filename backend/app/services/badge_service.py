from sqlalchemy.orm import Session

from app.models.badge import Badge
from app.models.user_badge import UserBadge
from app.models.volunteer import Volunteer


def check_and_award_badges(db: Session, volunteer: Volunteer):
    earned_badge_ids = {
        ub.badge_id for ub in db.query(UserBadge).filter(
            UserBadge.user_id == volunteer.user_id
        ).all()
    }

    eligible_badges = db.query(Badge).filter(
        Badge.points_required <= volunteer.points_total
    ).all()

    newly_awarded = []

    for badge in eligible_badges:
        if badge.id not in earned_badge_ids:
            user_badge = UserBadge(
                user_id=volunteer.user_id,
                badge_id=badge.id
            )
            db.add(user_badge)
            newly_awarded.append(user_badge)

    if newly_awarded:
        db.commit()
        for ub in newly_awarded:
            db.refresh(ub)

    return newly_awarded


def award_badge_manually(db: Session, user_id, badge_id):
    existing = db.query(UserBadge).filter(
        UserBadge.user_id == user_id,
        UserBadge.badge_id == badge_id
    ).first()

    if existing:
        return existing

    user_badge = UserBadge(
        user_id=user_id,
        badge_id=badge_id
    )

    db.add(user_badge)
    db.commit()
    db.refresh(user_badge)

    return user_badge
