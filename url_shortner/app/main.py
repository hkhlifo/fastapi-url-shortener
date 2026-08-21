from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import Base, engine, get_db


app = FastAPI(
    title="URL Shortener API",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


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


@app.post(
    "/shorten",
    response_model=schemas.URLResponse,
    status_code=201
)
def shorten_url(
    url_data: schemas.URLCreate,
    db: Session = Depends(get_db)
):
    original_url = str(url_data.url)

    existing_url = crud.get_url_by_original_url(
        db,
        original_url
    )

    if existing_url:
        return {
            "original_url": existing_url.original_url,
            "short_url": (
                f"http://127.0.0.1:8000/"
                f"{existing_url.short_code}"
            )
        }

    url = crud.create_short_url(
        db,
        original_url
    )

    return {
        "original_url": url.original_url,
        "short_url": (
            f"http://127.0.0.1:8000/"
            f"{url.short_code}"
        )
    }