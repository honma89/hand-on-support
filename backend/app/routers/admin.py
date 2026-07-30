from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User, UserStatus
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.volunteer import Volunteer
from app.models.address import Address

from app.schemas.admin import RoleAssign, UserStatusUpdate, TierAssign
from app.schemas.user import UserResponse
from app.schemas.volunteer import VolunteerResponse

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/volunteers", response_model=list[VolunteerResponse])
def list_volunteers(
    dzongkhag_id: str | None = None,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    query = db.query(Volunteer)

    if dzongkhag_id:
        query = query.join(
            Address, Address.id == Volunteer.address_id
        ).filter(Address.dzongkhag_id == dzongkhag_id)

    return query.all()


@router.get("/users/pending", response_model=list[UserResponse])
def list_pending_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return db.query(User).filter(
        User.status == UserStatus.PENDING
    ).all()


@router.patch("/users/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: str,
    status_update: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.status = status_update.status

    if status_update.status == UserStatus.REJECTED:
        user.rejected_at = datetime.now(timezone.utc)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/roles/assign")
def assign_role(
    role_assign: RoleAssign,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    role = db.query(Role).filter(Role.name == role_assign.role).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    existing = db.query(UserRole).filter(
        UserRole.user_id == role_assign.user_id,
        UserRole.role_id == role.id
    ).first()

    if existing:
        return {"detail": "Role already assigned"}

    user_role = UserRole(
        user_id=role_assign.user_id,
        role_id=role.id
    )

    db.add(user_role)
    db.commit()

    return {"detail": "Role assigned"}


@router.patch(
    "/volunteers/{volunteer_id}/tier",
    response_model=VolunteerResponse
)
def assign_tier(
    volunteer_id: str,
    tier_data: TierAssign,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    volunteer = db.query(Volunteer).filter(
        Volunteer.id == volunteer_id
    ).first()

    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    volunteer.tier_level_id = tier_data.tier_level_id

    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)

    return volunteer
