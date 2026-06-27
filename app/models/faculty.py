from datetime import datetime

from app import db


class Faculty(db.Model):

    __tablename__ = "faculty"

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

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    faculty_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    designation = db.Column(
        db.String(100),
        nullable=False
    )

    qualification = db.Column(
        db.String(150)
    )

    specialization = db.Column(
        db.String(150)
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    address = db.Column(
        db.Text
    )

    gender = db.Column(
        db.String(20)
    )

    joining_date = db.Column(
        db.Date
    )

    profile_image = db.Column(
        db.String(255),
        default="default.png"
    )

    status = db.Column(
        db.String(20),
        default="Active"
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
        back_populates="faculty",
        uselist=False
    )

    department = db.relationship(
        "Department",
        back_populates="faculty"
    )

    courses = db.relationship(
        "Course",
        back_populates="faculty",
        cascade="all, delete-orphan",
        lazy=True
    )

    feedbacks = db.relationship(
        "Feedback",
        back_populates="faculty",
        cascade="all, delete-orphan",
        lazy=True
    )

    
    def __repr__(self):

        return f"<Faculty {self.full_name}>"

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "department_id": self.department_id,
            "faculty_code": self.faculty_code,
            "full_name": self.full_name,
            "designation": self.designation,
            "qualification": self.qualification,
            "specialization": self.specialization,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "gender": self.gender,
            "joining_date": self.joining_date,
            "profile_image": self.profile_image,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }