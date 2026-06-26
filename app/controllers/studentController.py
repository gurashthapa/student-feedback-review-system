from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from app import db

from app.models.student import Student
from app.models.course import Course
from app.models.faculty import Faculty
from app.models.feedback import Feedback


class StudentController:

    @staticmethod
    @login_required
    def dashboard():

        student = Student.query.filter_by(user_id=current_user.id).first()

        total_courses = Course.query.count()

        total_feedback = Feedback.query.filter_by(
            student_id=student.id
        ).count()

        return render_template(
            "student/dashboard.html",
            student=student,
            total_courses=total_courses,
            total_feedback=total_feedback
        )

    @staticmethod
    @login_required
    def profile():

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        return render_template(
            "student/profile.html",
            student=student
        )

    @staticmethod
    @login_required
    def update_profile():

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        if request.method == "POST":

            student.phone = request.form.get("phone")
            student.address = request.form.get("address")
            student.year = request.form.get("year")
            student.semester = request.form.get("semester")

            db.session.commit()

            flash(
                "Profile updated successfully.",
                "success"
            )

            return redirect(
                url_for("student.profile")
            )

        return render_template(
            "student/profile.html",
            student=student
        )

    @staticmethod
    @login_required
    def course_list():

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        courses = Course.query.filter_by(
            department_id=student.department_id
        ).all()

        return render_template(
            "student/courses.html",
            courses=courses
        )

    @staticmethod
    @login_required
    def feedback_form(course_id):

        course = Course.query.get_or_404(course_id)

        faculty = Faculty.query.get(course.faculty_id)

        return render_template(
            "student/feedback.html",
            course=course,
            faculty=faculty
        )

    @staticmethod
    @login_required
    def submit_feedback(course_id):

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        course = Course.query.get_or_404(course_id)

        already_submitted = Feedback.query.filter_by(
            student_id=student.id,
            course_id=course.id
        ).first()

        if already_submitted:

            flash(
                "Feedback already submitted.",
                "warning"
            )

            return redirect(
                url_for("student.course_list")
            )

        rating = request.form.get("rating")

        review = request.form.get("review")

        anonymous = request.form.get("anonymous")

        feedback = Feedback(

            student_id=student.id,

            faculty_id=course.faculty_id,

            course_id=course.id,

            rating=rating,

            review=review,

            anonymous=True if anonymous else False

        )

        db.session.add(feedback)

        db.session.commit()

        flash(
            "Thank you for your feedback.",
            "success"
        )

        return redirect(
            url_for("student.history")
        )

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

    @staticmethod
    @login_required
    def delete_feedback(feedback_id):

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        feedback = Feedback.query.filter_by(
            id=feedback_id,
            student_id=student.id
        ).first()

        if feedback:

            db.session.delete(feedback)

            db.session.commit()

            flash(
                "Feedback deleted successfully.",
                "success"
            )

        else:

            flash(
                "Feedback not found.",
                "danger"
            )

        return redirect(
            url_for("student.history")
        )

    @staticmethod
    @login_required
    def statistics():

        student = Student.query.filter_by(
            user_id=current_user.id
        ).first()

        total_feedback = Feedback.query.filter_by(
            student_id=student.id
        ).count()

        average_rating = db.session.query(
            db.func.avg(Feedback.rating)
        ).filter_by(
            student_id=student.id
        ).scalar()

        if average_rating is None:
            average_rating = 0

        return render_template(
            "student/statistics.html",
            total_feedback=total_feedback,
            average_rating=round(average_rating, 2)
        )