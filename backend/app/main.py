from fastapi import FastAPI

from app.routers import users
from app.routers import auth
from app.routers import volunteers
from app.routers import locations
from app.routers import departments
from app.routers import events
from app.routers import activities
from app.routers import badges
from app.routers import leaderboard
from app.routers import recognitions
from app.routers import media
from app.routers import documents
from app.routers import announcements
from app.routers import donations
from app.routers import admin

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(volunteers.router)
app.include_router(locations.router)
app.include_router(departments.router)
app.include_router(events.router)
app.include_router(activities.router)
app.include_router(badges.router)
app.include_router(leaderboard.router)
app.include_router(recognitions.router)
app.include_router(media.router)
app.include_router(documents.router)
app.include_router(announcements.router)
app.include_router(donations.router)
app.include_router(admin.router)

@app.get("/api/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Liveness/readiness probe used by Docker/Nginx and uptime checks."""
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}


from app.routers import (  # noqa: E402
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
    users,
)

@app.get("/")
def root():
    return {
        "message": "Hand On Support API running"
    }
