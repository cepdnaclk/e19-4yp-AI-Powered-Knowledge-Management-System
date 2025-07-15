from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class UserProfile:
    """
    In-memory representation of a user.
    """
    user_id: str
    role: str
    interests: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # convenience helpers ------------
    def as_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "role": self.role,
            "interests": self.interests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_row(cls, row) -> "UserProfile":
        """Build from SQLAlchemy row object."""
        return cls(
            user_id=row.user_id,
            role=row.role,
            interests=row.interests.split(",") if row.interests else [],
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
