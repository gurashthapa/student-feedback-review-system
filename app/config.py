import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///feedback.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional settings
    DEBUG = True

    # Mail settings (for forgot password future use)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")