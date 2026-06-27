from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import all_blueprints

    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    # Import all models before creating tables
    from app.models import User, Student, Faculty, Department, Course, Feedback, Admin

    with app.app_context():
        db.create_all()

    return app