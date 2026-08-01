from app.models.address import Address
from app.models.user import User
from app.repositories.address_repository import AddressRepository
from app.schemas.location import AddressUpdate


class AddressService:
    def __init__(self, address_repo: AddressRepository):
        self.address_repo = address_repo

    async def set_user_address(self, user: User, data: AddressUpdate) -> Address:
        address = await self.address_repo.get_by_id(user.address_id) if user.address_id else None

        if address is None:
            address = Address(address_type=data.address_type)

        for field, value in data.model_dump(exclude_unset=True, exclude={"address_type"}).items():
            setattr(address, field, value)
        address.address_type = data.address_type

        address = await self.address_repo.create(address)
        user.address_id = address.id
        return address
