"""
Chandas Project — Flask Application Factory
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .config import config_by_name

# Extensions (initialized without app, bound later)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name=None):
    """Create and configure the Flask application."""

    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    # Ensure instance folder exists (for SQLite DB)
    os.makedirs(app.instance_path, exist_ok=True)

    # Ensure upload folder exists
    os.makedirs(app.config.get("UPLOAD_FOLDER", "uploads"), exist_ok=True)

    # Ensure cache folder exists
    os.makedirs(app.config.get("CACHE_DIR", "cache"), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from .routes.health import health_bp
    from .routes.chandas import chandas_bp
    from .routes.translate import translate_bp
    from .routes.ocr import ocr_bp
    from .routes.auth import auth_bp
    from .routes.history import history_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(chandas_bp, url_prefix="/api/chandas")
    app.register_blueprint(translate_bp, url_prefix="/api/translate")
    app.register_blueprint(ocr_bp, url_prefix="/api/ocr")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(history_bp, url_prefix="/api/history")

    # Create database tables
    with app.app_context():
        from . import models  # noqa: F401

        db.create_all()

    return app
