from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    Column,
    String,
    DateTime,
    create_engine,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from models.user_profile import UserProfile

DB_URL = "sqlite:///profiles.db"
Base = declarative_base()
_engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False)


class _ProfileRow(Base):
    __tablename__ = "user_profiles"

    user_id = Column(String, primary_key=True, index=True)
    role = Column(String, nullable=False)
    interests = Column(String, nullable=True)  # comma-separated
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


# create table on first import
Base.metadata.create_all(_engine)


# ---------- CRUD helpers ---------- #
def get(user_id: str) -> Optional[UserProfile]:
    with SessionLocal() as db:
        row = db.get(_ProfileRow, user_id)
        return UserProfile.from_row(row) if row else None


def create_or_update(
    user_id: str,
    role: str,
    interests: List[str],
) -> UserProfile:
    with SessionLocal() as db:
        row = db.get(_ProfileRow, user_id)
        now = datetime.utcnow()

        if row:
            row.role = role
            row.interests = ",".join(interests)
            row.updated_at = now
        else:
            row = _ProfileRow(
                user_id=user_id,
                role=role,
                interests=",".join(interests),
                created_at=now,
                updated_at=now,
            )
            db.add(row)
        db.commit()
        return UserProfile.from_row(row)
