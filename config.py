import os
from datetime import timedelta


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")


class Config:
    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key_change_me")

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(INSTANCE_DIR, "feedback.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session / Cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_HTTPONLY = True

    # JWT / Auth (if used later)
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt_dev_secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    # Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # Pagination
    ITEMS_PER_PAGE = 10


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}