"""Saved verse model — bookmarked verses with meter info."""

from datetime import datetime, timezone
from app import db


class SavedVerse(db.Model):
    """A verse bookmarked by the user."""

    __tablename__ = "saved_verses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    verse_text = db.Column(db.Text, nullable=False)
    transliteration = db.Column(db.Text, nullable=True)
    meter_name = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(200), nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "verse_text": self.verse_text,
            "transliteration": self.transliteration,
            "meter_name": self.meter_name,
            "notes": self.notes,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<SavedVerse {self.id}>"
