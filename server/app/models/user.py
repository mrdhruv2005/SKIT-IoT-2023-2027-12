"""User model for authentication."""

from datetime import datetime, timezone
from app import db


class User(db.Model):
    """User account for authentication and history tracking."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    analyses = db.relationship(
        "AnalysisHistory", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    saved_verses = db.relationship(
        "SavedVerse", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self):
        """Serialize user to dictionary (excluding password)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }

    def __repr__(self):
        return f"<User {self.username}>"
