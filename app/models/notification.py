from datetime import datetime

from app import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    recipient_role = db.Column(
        db.String(20),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=True
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "Student",
        backref="notifications"
    )