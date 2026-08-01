import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import get_settings

settings = get_settings()

# Files land in <UPLOAD_ROOT>/<subdir>/<uuid>.<ext> on local disk. Swapping
# this for S3/GCS later means replacing this one class -- UploadService
# and the router never touch the filesystem directly.
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


class UnsupportedFileTypeError(Exception):
    pass


class FileTooLargeError(Exception):
    pass


class FileStorageRepository:
    def __init__(self, upload_root: Path | None = None):
        self.upload_root = upload_root or Path(settings.UPLOAD_ROOT)

    async def save(self, file: UploadFile, subdir: str) -> str:
        """
        Saves an uploaded file to <upload_root>/<subdir>/<uuid>.<ext> and
        returns the URL path (e.g. "/uploads/events/<uuid>.jpg") the
        frontend can use directly as an <img src>.
        """
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise UnsupportedFileTypeError(
                f"Unsupported file type '{file.content_type}'. Allowed: JPEG, PNG, WebP."
            )

        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE_BYTES:
            raise FileTooLargeError("File exceeds the 5 MB upload limit.")

        extension = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
        }[file.content_type]

        # uuid4 filename -- never trust the client-provided filename (path
        # traversal, collisions, unicode weirdness all avoided this way).
        filename = f"{uuid.uuid4()}{extension}"
        target_dir = self.upload_root / subdir
        target_dir.mkdir(parents=True, exist_ok=True)

        target_path = target_dir / filename
        target_path.write_bytes(contents)

        return f"/uploads/{subdir}/{filename}"
