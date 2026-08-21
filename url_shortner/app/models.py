from sqlalchemy import Column, Integer, String

from app.database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)

    original_url = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    short_code = Column(
        String(10),
        nullable=False,
        unique=True,
        index=True
    )