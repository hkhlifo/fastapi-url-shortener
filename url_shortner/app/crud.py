import secrets
import string

from sqlalchemy.orm import Session

from app import models


def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


def get_url_by_original_url(
    db: Session,
    original_url: str
):
    return (
        db.query(models.URL)
        .filter(models.URL.original_url == original_url)
        .first()
    )


def get_url_by_short_code(
    db: Session,
    short_code: str
):
    return (
        db.query(models.URL)
        .filter(models.URL.short_code == short_code)
        .first()
    )


def create_short_url(
    db: Session,
    original_url: str
):
    short_code = generate_short_code()

    while get_url_by_short_code(db, short_code):
        short_code = generate_short_code()

    url = models.URL(
        original_url=original_url,
        short_code=short_code
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url