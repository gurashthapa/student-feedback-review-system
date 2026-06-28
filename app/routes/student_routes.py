import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app
)

from sqlalchemy import func
from werkzeug.utils import secure_filename

from app import db
from app.models.student import Student
from app.models.course import Course
from app.models.feedback import Feedback

student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)


def get_logged_student():

    if "user_id" not in session:
        return None

    return Student.query.filter_by(
        user_id=session["user_id"]
    ).first()


@student_bp.route("/dashboard")
def dashboard():

    student = get_logged_student()

    if student is None:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    total_feedback = Feedback.query.filter_by(
        student_id=student.id
    ).count()

    avg_rating = db.session.query(
        func.avg(Feedback.rating)
    ).filter(
        Feedback.student_id == student.id
    ).scalar()

    avg_rating = round(avg_rating, 2) if avg_rating else 0

    total_courses = Course.query.filter_by(
        department_id=student.department_id,
        semester=student.semester,
        status="Active"
    ).count()

    total_faculty = (
        db.session.query(Course.faculty_id)
        .filter(
            Course.department_id == student.department_id,
            Course.semester == student.semester,
            Course.status == "Active"
        )
        .distinct()
        .count()
    )

    recent_feedback = (
        Feedback.query
        .filter_by(student_id=student.id)
        .order_by(Feedback.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "student/dashboard.html",
        student=student,
        total_feedback=total_feedback,
        avg_rating=avg_rating,
        total_courses=total_courses,
        total_faculty=total_faculty,
        recent_feedback=recent_feedback
    )


@student_bp.route("/feedback", methods=["GET", "POST"])
def feedback():

    student = get_logged_student()

    if student is None:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    courses = Course.query.filter(
        Course.status == "Active"
    ).order_by(
        Course.course_name
    ).all()

    if request.method == "POST":

        course_id = request.form.get("course_id")
        rating = request.form.get("rating")
        review = request.form.get("review")
        anonymous = bool(request.form.get("anonymous"))

        if not course_id:
            flash("Please select a course.", "danger")
            return render_template(
                "student/feedback.html",
                student=student,
                courses=courses
            )

        if not rating:
            flash("Please select a rating.", "danger")
            return render_template(
                "student/feedback.html",
                student=student,
                courses=courses
            )

        if not review or review.strip() == "":
            flash("Please enter your review.", "danger")
            return render_template(
                "student/feedback.html",
                student=student,
                courses=courses
            )

        try:
            course = Course.query.get(int(course_id))
        except (ValueError, TypeError):
            course = None

        if course is None:
            flash("Selected course does not exist.", "danger")
            return render_template(
                "student/feedback.html",
                student=student,
                courses=courses
            )

        existing_feedback = Feedback.query.filter_by(
            student_id=student.id,
            course_id=course.id
        ).first()

        if existing_feedback:
            flash(
                "You have already submitted feedback for this course.",
                "warning"
            )
            return redirect(url_for("student.history"))

        feedback = Feedback(
            student_id=student.id,
            faculty_id=course.faculty_id,
            course_id=course.id,
            rating=int(rating),
            review=review.strip(),
            anonymous=anonymous,
            status="Pending"
        )

        db.session.add(feedback)
        db.session.commit()

        flash(
            "Feedback submitted successfully.",
            "success"
        )

        return redirect(url_for("student.history"))

    return render_template(
        "student/feedback.html",
        student=student,
        courses=courses
    )
@student_bp.route("/history")
def history():

    student = get_logged_student()

    if student is None:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    status = request.args.get("status")

    page = request.args.get("page", 1, type=int)
    per_page = 5

    query = Feedback.query.filter_by(student_id=student.id)

    if status:
        query = query.filter_by(status=status)

    feedbacks = (
        query
        .order_by(Feedback.created_at.desc())
        .paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    )

    return render_template(
        "student/history.html",
        student=student,
        feedbacks=feedbacks
    )


@student_bp.route("/history/<int:feedback_id>")
def view_feedback(feedback_id):

    student = get_logged_student()

    if student is None:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    feedback = Feedback.query.filter_by(
        id=feedback_id,
        student_id=student.id
    ).first()

    if feedback is None:
        flash("Feedback not found.", "danger")
        return redirect(url_for("student.history"))

    return render_template(
        "student/view_feedback.html",
        student=student,
        feedback=feedback
    )


@student_bp.route("/history/delete/<int:feedback_id>", methods=["POST"])
def delete_feedback(feedback_id):

    student = get_logged_student()

    if student is None:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    feedback = Feedback.query.filter_by(
        id=feedback_id,
        student_id=student.id
    ).first()

    if feedback is None:
        flash("Feedback not found.", "danger")
        return redirect(url_for("student.history"))

    if feedback.status.lower() != "pending":
        flash(
            "Only pending feedback can be deleted.",
            "warning"
        )
        return redirect(url_for("student.history"))

    db.session.delete(feedback)
    db.session.commit()

    flash(
        "Feedback deleted successfully.",
        "success"
    )

    return redirect(url_for("student.history"))

@student_bp.route("/profile", methods=["GET", "POST"])
def profile():

    student = get_logged_student()

    if student is None:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        file = request.files.get("profileImage")

        if file and file.filename != "":

            filename = secure_filename(file.filename)

            upload_folder = os.path.join(
                current_app.static_folder,
                "uploads"
            )

            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(upload_folder, filename)

            file.save(filepath)

            student.profile_image = filename

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        semester = request.form.get("semester")

        # User information
        if hasattr(student, "user") and student.user:

            if full_name:
                student.user.full_name = full_name

            if email:
                student.user.email = email

        # Student information
        if phone:
            student.phone = phone

        if address:
            student.address = address

        if semester:
            student.semester = int(semester)

        db.session.commit()

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(url_for("student.profile"))

    
    total_feedback = Feedback.query.filter_by(
        student_id=student.id
    ).count()

    avg_rating = db.session.query(
        func.avg(Feedback.rating)
    ).filter(
        Feedback.student_id == student.id
    ).scalar()

    avg_rating = round(avg_rating, 2) if avg_rating else 0

    total_courses = Course.query.filter_by(
        department_id=student.department_id,
        semester=student.semester,
        status="Active"
    ).count()

    total_faculty = (
        db.session.query(Course.faculty_id)
        .filter(
            Course.department_id == student.department_id,
            Course.semester == student.semester,
            Course.status == "Active"
        )
        .distinct()
        .count()
    )

    return render_template(
        "student/profile.html",
        student=student,
        total_feedback=total_feedback,
        avg_rating=avg_rating,
        total_courses=total_courses,
        total_faculty=total_faculty
    )


@student_bp.route("/courses")
def courses():

    student = get_logged_student()

    if student is None:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    courses = Course.query.filter_by(
        department_id=student.department_id,
        semester=student.semester,
        status="Active"
    ).all()

    return render_template(
        "student/courses.html",
        student=student,
        courses=courses
    )

@student_bp.route("/search")
def search():

    student = get_logged_student()

    if student is None:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    keyword = request.args.get("q", "").strip()

    feedbacks = []

    if keyword:

        feedbacks = (
            Feedback.query
            .join(Course)
            .join(Faculty)
            .filter(
                Feedback.student_id == student.id,
                or_(
                    Course.course_name.ilike(f"%{keyword}%"),
                    Course.course_code.ilike(f"%{keyword}%"),
                    Faculty.full_name.ilike(f"%{keyword}%"),
                    Feedback.review.ilike(f"%{keyword}%"),
                    Feedback.status.ilike(f"%{keyword}%")
                )
            )
            .all()
        )

    return render_template(
        "student/search_results.html",
        student=student,
        keyword=keyword,
        feedbacks=feedbacks
    )