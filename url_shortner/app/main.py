from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import crud, schemas
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


@app.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    url = crud.get_url_by_short_code(
        db,
        short_code
    )

    if not url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return RedirectResponse(
        url=url.original_url,
        status_code=307
    )