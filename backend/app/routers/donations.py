from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.donation import Donation

from app.schemas.donation import DonationCreate, DonationResponse

router = APIRouter(
    prefix="/donations",
    tags=["Donations"]
)


@router.post("", response_model=DonationResponse)
def create_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    new_donation = Donation(**donation.model_dump())

    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    return new_donation


@router.get("", response_model=list[DonationResponse])
def list_donations(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return db.query(Donation).order_by(Donation.created_at.desc()).all()
