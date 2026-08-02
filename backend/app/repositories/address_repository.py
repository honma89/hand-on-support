import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address import Address
from app.models.dzongkhag import Dzongkhag


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

    async def save(self, address: Address) -> Address:
        await self.db.flush()
        await self.db.refresh(address)
        return address

    async def get_dzongkhag_name(self, address_id: uuid.UUID) -> str | None:
        """Resolves an address straight to its dzongkhag's name, for
        callers (like events-near-me) that just need the location label
        and don't want to juggle two lookups."""
        result = await self.db.execute(
            select(Dzongkhag.name)
            .select_from(Address)
            .join(Dzongkhag, Dzongkhag.id == Address.dzongkhag_id)
            .where(Address.id == address_id)
        )
        return result.scalar_one_or_none()
