from sqlalchemy.orm import Session

from app.models.address import Address
from app.models.user import User
from app.models.volunteer import Volunteer
from app.repositories.address_repository import AddressRepository
from app.schemas.address import AddressCreate
from app.schemas.location import AddressUpdate


def set_volunteer_address(
    db: Session,
    volunteer: Volunteer,
    data: AddressCreate
):
    """Legacy/sync helper - only used by the unwired app/routers/volunteers.py
    (not included in main.py). Left as-is; not part of the live async stack."""
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


class AddressService:
    """What the live app.routers.users PUT /users/me/address endpoint uses."""

    def __init__(self, address_repo: AddressRepository):
        self.address_repo = address_repo

    async def set_user_address(self, user: User, data: AddressUpdate) -> Address:
        address = await self.address_repo.get_by_id(user.address_id) if user.address_id else None
        is_new = address is None
        if is_new:
            address = Address()

        address.address_type = data.address_type
        address.dzongkhag_id = data.dzongkhag_id
        address.dungkhag_id = data.dungkhag_id
        address.gewog_id = data.gewog_id
        address.village = data.village
        address.full_address = data.additional_details

        if is_new:
            address = await self.address_repo.create(address)
        else:
            address = await self.address_repo.save(address)

        if user.address_id != address.id:
            user.address_id = address.id

        return address
