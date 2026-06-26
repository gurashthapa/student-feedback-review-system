from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func

from app import db
from app.models.user import User
from app.models.faculty import Faculty
from app.models.course import Course
from app.models.feedback import Feedback


class FacultyController:

    # ==========================================
    # Faculty Dashboard
    # ==========================================
    @staticmethod
    @login_required
    def dashboard():

        faculty = Faculty.query.filter_by(
            user_id=current_user.id
        ).first()

        total_courses = Course.query.filter_by(
            faculty_id=faculty.id
        ).count()

        total_feedback = Feedback.query.filter_by(
            faculty_id=faculty.id
        ).count()

        average_rating = db.session.query(
            func.avg(Feedback.rating)
        ).filter_by(
            faculty_id=faculty.id
        ).scalar()

        if average_rating is None:
            average_rating = 0

        recent_feedback = Feedback.query.filter_by(
            faculty_id=faculty.id
        ).order_by(
            Feedback.created_at.desc()
        ).limit(5).all()

        return render_template(
            "faculty/dashboard.html",
            faculty=faculty,
            total_courses=total_courses,
            total_feedback=total_feedback,
            average_rating=round(average_rating, 2),
            recent_feedback=recent_feedback
        )

    # ==========================================
    # Faculty Profile
    # ==========================================
    @staticmethod
    @login_required
    def profile():

        faculty = Faculty.query.filter_by(
            user_id=current_user.id
        ).first()

        return render_template(
            "faculty/profile.html",
            faculty=faculty
        )

    # ==========================================
    # Update Profile
    # ==========================================
    @staticmethod
    @login_required
    def update_profile():

        faculty = Faculty.query.filter_by(
            user_id=current_user.id
        ).first()

        if request.method == "POST":

            faculty.phone = request.form.get("phone")
            faculty.address = request.form.get("address")
            faculty.designation = request.form.get("designation")

            db.session.commit()

            flash(
                "Profile updated successfully.",
                "success"
            )

            return redirect(
                url_for("faculty.profile")
            )

        return render_template(
            "faculty/profile.html",
            faculty=faculty
        )

    # ==========================================
    # View Assigned Courses
    # ==========================================
    @staticmethod
    @login_required
    def courses():

        faculty = Faculty.query.filter_by(
            user_id=current_user.id
        ).first()

        courses = Course.query.filter_by(
            faculty_id=faculty.id
        ).all()

        return render_template(
            "faculty/courses.html",
            courses=courses
        )

    # ==========================================
    # View Feedback
    # ==========================================
    @staticmethod
    @login_required
    def feedbacks():

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
    # Feedback Details
    # ==========================================
    @staticmethod
    @login_required
    def feedback_details(feedback_id):

        feedback = Feedback.query.get_or_404(
            feedback_id
        )

        return render_template(
            "faculty/feedback_details.html",
            feedback=feedback
        )

    # ==========================================
    # Search Feedback
    # ==========================================
    @staticmethod
    @login_required
    def search_feedback():

        faculty = Faculty.query.filter_by(
            user_id=current_user.id
        ).first()

        keyword = request.args.get(
            "keyword",
            ""
        )

        feedbacks = Feedback.query.filter(
            Feedback.faculty_id == faculty.id,
            Feedback.review.contains(keyword)
        ).all()

        return render_template(
            "faculty/feedbacks.html",
            feedbacks=feedbacks,
            keyword=keyword
        )

    # ==========================================
    # Faculty Statistics
    # ==========================================
    @staticmethod
    @login_required
    def statistics():

        faculty = Faculty.query.filter_by(
            user_id=current_user.id
        ).first()

        total_feedback = Feedback.query.filter_by(
            faculty_id=faculty.id
        ).count()

        average_rating = db.session.query(
            func.avg(Feedback.rating)
        ).filter_by(
            faculty_id=faculty.id
        ).scalar()

        if average_rating is None:
            average_rating = 0

        five_star = Feedback.query.filter_by(
            faculty_id=faculty.id,
            rating=5
        ).count()

        four_star = Feedback.query.filter_by(
            faculty_id=faculty.id,
            rating=4
        ).count()

        three_star = Feedback.query.filter_by(
            faculty_id=faculty.id,
            rating=3
        ).count()

        two_star = Feedback.query.filter_by(
            faculty_id=faculty.id,
            rating=2
        ).count()

        one_star = Feedback.query.filter_by(
            faculty_id=faculty.id,
            rating=1
        ).count()

        return render_template(
            "faculty/statistics.html",
            total_feedback=total_feedback,
            average_rating=round(average_rating, 2),
            five_star=five_star,
            four_star=four_star,
            three_star=three_star,
            two_star=two_star,
            one_star=one_star
        )

    # ==========================================
    # View All Faculty (Admin)
    # ==========================================
    @staticmethod
    @login_required
    def index():

        faculty_list = Faculty.query.order_by(
            Faculty.id.desc()
        ).all()

        return render_template(
            "admin/faculty.html",
            faculty_list=faculty_list
        )

    # ==========================================
    # Delete Faculty (Admin)
    # ==========================================
    @staticmethod
    @login_required
    def delete(faculty_id):

        faculty = Faculty.query.get_or_404(
            faculty_id
        )

        db.session.delete(faculty)
        db.session.commit()

        flash(
            "Faculty deleted successfully.",
            "success"
        )

        return redirect(
            url_for("faculty.index")
        )