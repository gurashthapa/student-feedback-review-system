from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secret-key"

    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "mysql+pymysql://root:gurash123@localhost/std_feedback"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import all_blueprints

    for bp in all_blueprints:
        app.register_blueprint(bp)

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    return app