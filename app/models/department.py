from datetime import datetime

from app import db


class Department(db.Model):

    __tablename__ = "departments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    department_name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    department_code = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    description = db.Column(
        db.Text
    )

    hod_name = db.Column(
        db.String(100)
    )

    office_location = db.Column(
        db.String(100)
    )

    contact_email = db.Column(
        db.String(120)
    )

    contact_phone = db.Column(
        db.String(20)
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

    
    students = db.relationship(
        "Student",
        back_populates="department",
        cascade="all, delete-orphan",
        lazy=True
    )

    faculty = db.relationship(
        "Faculty",
        back_populates="department",
        cascade="all, delete-orphan",
        lazy=True
    )

    courses = db.relationship(
        "Course",
        back_populates="department",
        cascade="all, delete-orphan",
        lazy=True
    )

    @property
    def name(self):
        return self.department_name

    
    def __repr__(self):
        return f"<Department {self.department_name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "department_name": self.department_name,
            "department_code": self.department_code,
            "description": self.description,
            "hod_name": self.hod_name,
            "office_location": self.office_location,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }