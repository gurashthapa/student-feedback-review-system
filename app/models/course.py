from datetime import datetime

from app import db


class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    course_name = db.Column(
        db.String(100),
        nullable=False
    )

    course_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculty.id"),
        nullable=False
    )

    semester = db.Column(
        db.Integer,
        nullable=False
    )

    credit = db.Column(
        db.Integer,
        nullable=False
    )

    description = db.Column(
        db.Text
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

    # ==========================
    # Relationships
    # ==========================

    department = db.relationship(
        "Department",
        back_populates="courses"
    )

    faculty = db.relationship(
        "Faculty",
        back_populates="courses"
    )

    feedbacks = db.relationship(
        "Feedback",
        back_populates="course",
        cascade="all, delete-orphan",
        lazy=True
    )

    # ==========================
    # Helper Methods
    # ==========================

    def __repr__(self):

        return f"<Course {self.course_name}>"

    def to_dict(self):

        return {
            "id": self.id,
            "course_name": self.course_name,
            "course_code": self.course_code,
            "department_id": self.department_id,
            "faculty_id": self.faculty_id,
            "semester": self.semester,
            "credit": self.credit,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }