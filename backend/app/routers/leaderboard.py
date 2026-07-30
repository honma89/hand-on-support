from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.volunteer import Volunteer
from app.models.address import Address

from app.schemas.badge import LeaderboardEntry

router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"]
)


@router.get("", response_model=list[LeaderboardEntry])
def get_leaderboard(
    dzongkhag_id: str | None = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Volunteer)

    if dzongkhag_id:
        query = query.join(
            Address, Address.id == Volunteer.address_id
        ).filter(Address.dzongkhag_id == dzongkhag_id)

    volunteers = query.order_by(
        Volunteer.points_total.desc()
    ).limit(limit).all()

    return [
        LeaderboardEntry(
            volunteer_id=v.id,
            firstname=v.firstname,
            lastname=v.lastname,
            points_total=v.points_total,
            hours_total=float(v.hours_total)
        )
        for v in volunteers
    ]
