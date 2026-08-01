from fastapi import UploadFile

from app.core.exceptions import ValidationError
from app.repositories.file_storage_repository import (
    FileStorageRepository,
    FileTooLargeError,
    UnsupportedFileTypeError,
)


class UploadService:
    def __init__(self, storage_repo: FileStorageRepository):
        self.storage_repo = storage_repo

    async def upload_event_image(self, file: UploadFile) -> str:
        try:
            return await self.storage_repo.save(file, subdir="events")
        except (UnsupportedFileTypeError, FileTooLargeError) as e:
            raise ValidationError(str(e))
