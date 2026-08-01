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
    home,
    leaderboard,
    locations,
    notifications,
    point_bank,
    registrations,
    uploads,
    users,
)
# NOTE (disabled): announcements, departments, documents, donations,
# media, recognitions -- see the comment further below, these still
# crash on import (broken legacy sync DB/auth stack). `locations` was
# fixed and re-enabled below.

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
app.include_router(home.router, prefix=settings.API_V1_PREFIX)
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

# NOTE (disabled): these 7 routers are NOT actually on the async stack
# despite the comment that used to sit here. Every one of them still
# imports `app.database.session` (a synchronous SQLAlchemy engine built
# with `create_engine(DATABASE_URL)` against a `postgresql+asyncpg://`
# URL -- asyncpg has no sync driver, and psycopg2 isn't even in
# requirements.txt) and `app.core.dependencies` (a separate auth layer
# requiring SECRET_KEY/ALGORITHM env vars that don't exist in
# .env.example). Importing any of them crashes the app at startup.
# Commented out so the rest of the app actually boots; see the
# continuation prompt for porting these properly onto app.db.session /
# app.deps before re-enabling.
# app.include_router(locations.router, prefix=settings.API_V1_PREFIX)
# app.include_router(departments.router, prefix=settings.API_V1_PREFIX)
# app.include_router(media.router, prefix=settings.API_V1_PREFIX)
# app.include_router(documents.router, prefix=settings.API_V1_PREFIX)
# app.include_router(announcements.router, prefix=settings.API_V1_PREFIX)
# app.include_router(donations.router, prefix=settings.API_V1_PREFIX)
# app.include_router(recognitions.router, prefix=settings.API_V1_PREFIX)
app.include_router(locations.router, prefix=settings.API_V1_PREFIX)


@app.get("/api/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Liveness/readiness probe used by Docker/Nginx and uptime checks."""
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}


@app.get("/")
def root():
    return {"message": "Hand On Support API running"}
