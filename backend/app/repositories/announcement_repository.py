from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.announcement import Announcement


class AnnouncementRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self) -> list[Announcement]:
        result = await self.db.execute(
            select(Announcement).order_by(Announcement.created_at.desc())
        )
        return list(result.scalars().all())
