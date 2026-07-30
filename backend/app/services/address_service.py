from sqlalchemy.orm import Session

from app.models.address import Address
from app.models.volunteer import Volunteer
from app.schemas.address import AddressCreate


def set_volunteer_address(
    db: Session,
    volunteer: Volunteer,
    data: AddressCreate
):
    if volunteer.address_id:
        address = db.query(Address).filter(
            Address.id == volunteer.address_id
        ).first()
    else:
        address = Address()

    address.address_type = data.address_type
    address.dzongkhag_id = data.dzongkhag_id
    address.dungkhag_id = data.dungkhag_id
    address.gewog_id = data.gewog_id
    address.village = data.village
    address.full_address = data.additional_details

    db.add(address)
    db.commit()
    db.refresh(address)

    volunteer.address_id = address.id
    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)

    return address
