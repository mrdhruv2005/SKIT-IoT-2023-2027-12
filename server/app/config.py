import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-dev-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours in seconds

    # API Keys
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

    # File upload
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max upload
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "uploads"
    )

    # Cache
    CACHE_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "cache"
    )
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    # Meter database path
    METER_DATA_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "meters"
    )

    # Sandhi data path
    SANDHI_DATA_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "sandhi"
    )


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True

    @staticmethod
    def _get_dev_db_uri():
        """Get database URI, falling back to SQLite if DATABASE_URL is empty."""
        url = os.environ.get("DATABASE_URL", "")
        if url:
            return url
        return "sqlite:///" + os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "instance", "chandas_dev.db"
        )

    SQLALCHEMY_DATABASE_URI = _get_dev_db_uri()


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")

    # Fix Render's postgres:// URI (SQLAlchemy requires postgresql://)
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
