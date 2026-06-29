from datetime import datetime

from app import db

class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    employee_id = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    designation = db.Column(
        db.String(100)
    )

    office = db.Column(
        db.String(100)
    )

    profile_image = db.Column(
        db.String(255),
        default="default.png"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="admin",
        lazy=True
    )

    def __repr__(self):
        return f"<Admin {self.full_name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "employee_id": self.employee_id,
            "full_name": self.full_name,
            "phone": self.phone,
            "designation": self.designation,
            "office": self.office,
            "profile_image": self.profile_image,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }