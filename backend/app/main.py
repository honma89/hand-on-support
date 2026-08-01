from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.routers import (
    admin,
    analytics,
    attendance,
    auth,
    badges,
    events,
    leaderboard,
    notifications,
    point_bank,
    registrations,
    uploads,
    users,
)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(events.router, prefix=settings.API_V1_PREFIX)
app.include_router(registrations.router, prefix=settings.API_V1_PREFIX)
app.include_router(attendance.router, prefix=settings.API_V1_PREFIX)
app.include_router(badges.router, prefix=settings.API_V1_PREFIX)
app.include_router(leaderboard.router, prefix=settings.API_V1_PREFIX)
app.include_router(point_bank.router, prefix=settings.API_V1_PREFIX)
app.include_router(notifications.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin.router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX)
app.include_router(uploads.router, prefix=settings.API_V1_PREFIX)

# Serve uploaded files directly. In docker-compose this directory is a
# mounted volume so files survive container rebuilts; see UPLOAD_ROOT in
# core/config.py. NOT suitable for a multi-instance/production deploy as-is
# (each instance would have its own local disk) -- swap FileStorageRepository
# for S3/GCS before scaling horizontally.
_upload_root = Path(settings.UPLOAD_ROOT)
_upload_root.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(_upload_root)), name="uploads")


@app.get("/api/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Liveness/readiness probe used by Docker/Nginx and uptime checks."""
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}


@app.get("/")
def root():
    return {"message": "Hand On Support API running"}
