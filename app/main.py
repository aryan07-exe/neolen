from fastapi import FastAPI
from app.api.routes import router
from app.db.mongodb import mongodb
from app.core.config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await mongodb.connect_db()
    yield
    # Shutdown
    await mongodb.close_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "AI Health Tracking API is running"}
