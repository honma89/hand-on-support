from fastapi import FastAPI
from app.routers import users
from app.routers import auth




app = FastAPI(
    title="Hand On Support API"
)

app.include_router(auth.router)

app.include_router(users.router)


@app.get("/")
def root():
    return {
        "message": "Hand On Support API running"
    }