"""
Database models — imports all models so Flask-Migrate can detect them.
"""

from .user import User  # noqa: F401
from .analysis import AnalysisHistory  # noqa: F401
from .verse import SavedVerse  # noqa: F401
