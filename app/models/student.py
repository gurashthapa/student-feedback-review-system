from datetime import datetime

from app import db


class Student(db.Model):
    __tablename__ = "students"

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

    student_id = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
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
        db.String(10)
    )

    date_of_birth = db.Column(
        db.Date
    )

    year = db.Column(
        db.Integer,
        nullable=False
    )

    semester = db.Column(
        db.Integer,
        nullable=False
    )

    section = db.Column(
        db.String(10)
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
        back_populates="student",
        uselist=False
    )

    department = db.relationship(
        "Department",
        back_populates="students"
    )

    feedbacks = db.relationship(
        "Feedback",
        back_populates="student",
        cascade="all, delete-orphan",
        lazy=True
    )


    @property
    def current_year(self):
        return f"Year {self.year}"

    @property
    def current_semester(self):
        return f"Semester {self.semester}"


    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "user_id": self.user_id,
            "department_id": self.department_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "year": self.year,
            "semester": self.semester,
            "section": self.section,
            "profile_image": self.profile_image,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Student {self.full_name}>"