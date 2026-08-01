import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address import Address


class AddressRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, address_id: uuid.UUID) -> Address | None:
        return await self.db.get(Address, address_id)

    async def create(self, address: Address) -> Address:
        self.db.add(address)
        await self.db.flush()
        await self.db.refresh(address)
        return address
