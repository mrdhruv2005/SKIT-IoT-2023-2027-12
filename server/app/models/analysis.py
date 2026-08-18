"""Analysis history model — stores past chandas analyses, translations, and OCR results."""

from datetime import datetime, timezone
from app import db


class AnalysisHistory(db.Model):
    """Stores a user's past analysis results."""

    __tablename__ = "analysis_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    analysis_type = db.Column(
        db.String(20), nullable=False
    )  # 'chandas', 'translation', 'ocr'
    input_text = db.Column(db.Text, nullable=False)
    result_json = db.Column(db.JSON, nullable=False)  # Full analysis result
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )

    def to_dict(self):
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "analysis_type": self.analysis_type,
            "input_text": self.input_text,
            "result": self.result_json,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<AnalysisHistory {self.id} ({self.analysis_type})>"
