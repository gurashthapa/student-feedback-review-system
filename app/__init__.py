from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from config import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    # Add this
    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.root_path,
        "static",
        "uploads"
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import all_blueprints

    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    from app.models import User, Student, Faculty, Department, Course, Feedback, Admin

    with app.app_context():
        db.create_all()

    return app