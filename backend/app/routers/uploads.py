from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.core.exceptions import ValidationError
from app.deps import require_organizer_or_admin
from app.repositories.file_storage_repository import FileStorageRepository
from app.schemas.upload import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter(prefix="/uploads", tags=["uploads"], dependencies=[Depends(require_organizer_or_admin)])


def get_upload_service() -> UploadService:
    return UploadService(FileStorageRepository())


@router.post("/event-image", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_event_image(
    file: UploadFile,
    service: UploadService = Depends(get_upload_service),
):
    try:
        url = await service.upload_event_image(file)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    return UploadResponse(url=url)
