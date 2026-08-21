from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app import models


app = FastAPI(
    title="URL Shortener API",
    version="1.0.0"
)


models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {
        "message": "URL Shortener API is running"
    }


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }