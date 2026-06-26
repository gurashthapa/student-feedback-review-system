from datetime import datetime

from app import db


class Feedback(db.Model):

    __tablename__ = "feedback"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculty.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    review = db.Column(
        db.Text,
        nullable=False
    )

    anonymous = db.Column(
        db.Boolean,
        default=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
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

    # ==========================================
    # Relationships
    # ==========================================

    student = db.relationship(
        "Student",
        back_populates="feedbacks"
    )

    faculty = db.relationship(
        "Faculty",
        back_populates="feedbacks"
    )

    course = db.relationship(
        "Course",
        back_populates="feedbacks"
    )

    # ==========================================
    # Helper Methods
    # ==========================================

    def __repr__(self):

        return f"<Feedback {self.id}>"

    @property
    def rating_text(self):

        ratings = {
            1: "Poor",
            2: "Fair",
            3: "Good",
            4: "Very Good",
            5: "Excellent"
        }

        return ratings.get(self.rating, "Not Rated")

    def to_dict(self):

        return {
            "id": self.id,
            "student_id": self.student_id,
            "faculty_id": self.faculty_id,
            "course_id": self.course_id,
            "rating": self.rating,
            "rating_text": self.rating_text,
            "review": self.review,
            "anonymous": self.anonymous,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }