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

DB_URL = "sqlite:///profiles.db"  # location for datasbase profile.
Base = declarative_base()
_engine = create_engine(DB_URL, echo=False, future=True)  # using SQLite — a lightweight, file-based database management system.
SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False)

# Provides CRUD operations for managing UserProfile data in a SQLite database using SQLAlchemy


class _ProfileRow(Base):
    __tablename__ = "user_profiles"

    user_id = Column(String, primary_key=True, index=True)
    role = Column(String, nullable=False)
    interests = Column(String, nullable=True)  # comma-separated
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


# create table on first import
#This creates the table based on the _ProfileRow class (which is an ORM model) if it doesn’t already exist.
Base.metadata.create_all(_engine)


# ---------- CRUD helpers ---------- #
def get(user_id: str) -> Optional[UserProfile]:
    with SessionLocal() as db:
        row = db.get(_ProfileRow, user_id)
        return UserProfile.from_row(row) if row else None

#If the user exists → update role/interests, Else → create a new entry, Commits changes and returns a UserProfile.
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
