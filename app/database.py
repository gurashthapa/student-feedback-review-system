from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "mysql+pymysql://root:gurash123@localhost/student_feedback"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


def save_to_db(instance):
    db.session.add(instance)
    db.session.commit()


def delete_from_db(instance):
    db.session.delete(instance)
    db.session.commit()


def rollback_db():
    db.session.rollback()