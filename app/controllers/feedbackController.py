from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func

from app import db
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.course import Course
from app.models.feedback import Feedback


class FeedbackController:

    # ==========================================
    # View All Feedback (Admin)
    # ==========================================
    @staticmethod
    @login_required
    def index():

        feedbacks = Feedback.query.order_by(
            Feedback.created_at.desc()
        ).all()

        return render_template(
            "admin/feedback.html",
            feedbacks=feedbacks
        )

    # ==========================================
    # Feedback Form
    # ==========================================
    @staticmethod
    @login_required
    def create(course_id):

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        course = Course.query.get_or_404(course_id)

        faculty = Faculty.query.get_or_404(
            course.faculty_id
        )

        existing = Feedback.query.filter_by(
            student_id=student.id,
            course_id=course.id
        ).first()

        if existing:

            flash(
                "You have already submitted feedback for this course.",
                "warning"
            )

            return redirect(
                url_for("student.dashboard")
            )

        return render_template(
            "student/feedback.html",
            course=course,
            faculty=faculty
        )

    # ==========================================
    # Save Feedback
    # ==========================================
    @staticmethod
    @login_required
    def store(course_id):

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        course = Course.query.get_or_404(course_id)

        feedback = Feedback(

            student_id=student.id,

            faculty_id=course.faculty_id,

            course_id=course.id,

            rating=int(request.form.get("rating")),

            review=request.form.get("review"),

            anonymous=True if request.form.get("anonymous") else False

        )

        db.session.add(feedback)
        db.session.commit()

        flash(
            "Feedback submitted successfully.",
            "success"
        )

        return redirect(
            url_for("student.history")
        )

    # ==========================================
    # Student Feedback History
    # ==========================================
    @staticmethod
    @login_required
    def history():

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        feedbacks = Feedback.query.filter_by(
            student_id=student.id
        ).order_by(
            Feedback.created_at.desc()
        ).all()

        return render_template(
            "student/history.html",
            feedbacks=feedbacks
        )

    # ==========================================
    # Edit Feedback
    # ==========================================
    @staticmethod
    @login_required
    def edit(feedback_id):

        feedback = Feedback.query.get_or_404(
            feedback_id
        )

        if request.method == "POST":

            feedback.rating = int(
                request.form.get("rating")
            )

            feedback.review = request.form.get(
                "review"
            )

            feedback.anonymous = True if request.form.get(
                "anonymous"
            ) else False

            db.session.commit()

            flash(
                "Feedback updated successfully.",
                "success"
            )

            return redirect(
                url_for("feedback.history")
            )

        return render_template(
            "student/edit_feedback.html",
            feedback=feedback
        )

    # ==========================================
    # Delete Feedback
    # ==========================================
    @staticmethod
    @login_required
    def delete(feedback_id):

        feedback = Feedback.query.get_or_404(
            feedback_id
        )

        db.session.delete(feedback)
        db.session.commit()

        flash(
            "Feedback deleted successfully.",
            "success"
        )

        return redirect(
            url_for("feedback.history")
        )

    # ==========================================
    # Search Feedback
    # ==========================================
    @staticmethod
    @login_required
    def search():

        keyword = request.args.get(
            "keyword",
            ""
        )

        feedbacks = Feedback.query.filter(
            Feedback.review.contains(keyword)
        ).all()

        return render_template(
            "admin/feedback.html",
            feedbacks=feedbacks,
            keyword=keyword
        )

    # ==========================================
    # Filter by Rating
    # ==========================================
    @staticmethod
    @login_required
    def filter_by_rating(rating):

        feedbacks = Feedback.query.filter_by(
            rating=rating
        ).all()

        return render_template(
            "admin/feedback.html",
            feedbacks=feedbacks
        )

    # ==========================================
    # Faculty Feedback
    # ==========================================
    @staticmethod
    @login_required
    def faculty_feedback():

        faculty = Faculty.query.filter_by(
            user_id=current_user.id
        ).first()

        feedbacks = Feedback.query.filter_by(
            faculty_id=faculty.id
        ).order_by(
            Feedback.created_at.desc()
        ).all()

        return render_template(
            "faculty/feedbacks.html",
            feedbacks=feedbacks
        )

    # ==========================================
    # Feedback Statistics
    # ==========================================
    @staticmethod
    @login_required
    def statistics():

        total_feedback = Feedback.query.count()

        average_rating = db.session.query(
            func.avg(Feedback.rating)
        ).scalar()

        if average_rating is None:
            average_rating = 0

        five_star = Feedback.query.filter_by(
            rating=5
        ).count()

        four_star = Feedback.query.filter_by(
            rating=4
        ).count()

        three_star = Feedback.query.filter_by(
            rating=3
        ).count()

        two_star = Feedback.query.filter_by(
            rating=2
        ).count()

        one_star = Feedback.query.filter_by(
            rating=1
        ).count()

        return render_template(
            "admin/feedback_statistics.html",
            total_feedback=total_feedback,
            average_rating=round(average_rating, 2),
            five_star=five_star,
            four_star=four_star,
            three_star=three_star,
            two_star=two_star,
            one_star=one_star
        )
    