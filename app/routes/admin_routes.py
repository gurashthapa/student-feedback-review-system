from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from sqlalchemy import func

from app import db
from app.models import (
    Student,
    Faculty,
    Course,
    Department,
    Feedback,
)

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Unauthorized access. Please login as admin.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def get_dashboard_stats():

    total_students = Student.query.count()
    total_faculty = Faculty.query.count()
    total_courses = Course.query.count()
    total_departments = Department.query.count()
    total_feedback = Feedback.query.count()

    avg_rating = db.session.query(func.avg(Feedback.rating)).scalar() or 0

    rating_values = [
        Feedback.query.filter_by(rating=1).count(),
        Feedback.query.filter_by(rating=2).count(),
        Feedback.query.filter_by(rating=3).count(),
        Feedback.query.filter_by(rating=4).count(),
        Feedback.query.filter_by(rating=5).count(),
    ]

    distribution_values = [
        Feedback.query.filter_by(status="Pending").count(),
        Feedback.query.filter_by(status="Approved").count(),
        Feedback.query.filter_by(status="Rejected").count(),
    ]

    recent_feedback = (
        Feedback.query.order_by(Feedback.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "total_students": total_students,
        "total_faculty": total_faculty,
        "total_courses": total_courses,
        "total_departments": total_departments,
        "total_feedback": total_feedback,
        "avg_rating": round(avg_rating, 2),
        "rating_labels": ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"],
        "rating_values": rating_values,
        "distribution_labels": ["Pending", "Approved", "Rejected"],
        "distribution_values": distribution_values,
        "recent_feedback": recent_feedback,
    }


@admin_bp.route("/")
@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    data = get_dashboard_stats()
    return render_template("admin/dashboard.html", **data)


@admin_bp.route("/students")
@admin_required
def students():
    students = Student.query.order_by(Student.id.desc()).all()
    departments = Department.query.order_by(Department.department_name).all()

    return render_template(
        "admin/students.html",
        students=students,
        departments=departments,
    )

@admin_bp.route("/students/add", methods=["GET", "POST"])
@admin_required
def add_student():
    departments = Department.query.order_by(Department.department_name).all()

    if request.method == "POST":
        student = Student(
    student_id=request.form.get("student_id"),
    full_name=request.form.get("full_name"),
    email=request.form.get("email"),
    department_id=request.form.get("department_id"),
    year=request.form.get("year"),
    semester=request.form.get("semester"),
    user_id=1
)
    
        db.session.add(student)
        db.session.commit()
        flash("Student added successfully.", "success")
        return redirect(url_for("admin.students"))

    return render_template("admin/add_student.html", departments=departments)


@admin_bp.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    departments = Department.query.order_by(Department.department_name).all()

    if request.method == "POST":
        student.student_id = request.form.get("student_id")
        student.full_name = request.form.get("full_name")
        student.email = request.form.get("email")
        student.department_id = request.form.get("department_id")
        student.semester = request.form.get("semester")

        db.session.commit()
        flash("Student updated successfully.", "success")
        return redirect(url_for("admin.students"))

    return render_template("admin/edit_student.html", student=student, departments=departments)


@admin_bp.route("/students/<int:student_id>/delete", methods=["POST"])
@admin_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully.", "success")
    return redirect(url_for("admin.students"))


@admin_bp.route("/faculty")
@admin_required
def faculty():

    faculty_list = Faculty.query.order_by(
        Faculty.full_name
    ).all()

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    return render_template(
        "admin/faculty.html",
        faculty_list=faculty_list,
        departments=departments
    )

from app.models.user import User
if request.method == "POST":

    department_id = request.form.get("department_id")

    user = User(
        username=request.form.get("username"),
        email=request.form.get("email"),
        role="faculty"
    )

    user.set_password(request.form.get("password"))

    db.session.add(user)
    db.session.flush()

    faculty = Faculty(
        user_id=user.id,
        department_id=int(department_id),
        faculty_code=f"FAC{user.id:03d}",
        full_name=request.form.get("name"),
        designation=request.form.get("designation"),
        email=request.form.get("email")
    )

    db.session.add(faculty)
    db.session.commit()

    flash("Faculty added successfully.", "success")
    return redirect(url_for("admin.faculty"))

@admin_bp.route("/faculty/add", methods=["GET", "POST"])
@admin_required
def add_faculty():

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    if request.method == "POST":

        department_id = request.form.get("department_id")

        if not department_id:
            flash("Please select a department.", "danger")
            return redirect(url_for("admin.faculty"))

        # Check if username already exists
        if User.query.filter_by(username=request.form.get("username")).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("admin.faculty"))

        # Check if email already exists
        if User.query.filter_by(email=request.form.get("email")).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("admin.faculty"))

        user = User(
            username=request.form.get("username"),
            email=request.form.get("email"),
            role="faculty"
        )

        user.set_password(request.form.get("password"))

        db.session.add(user)
        db.session.flush()

        faculty = Faculty(
            user_id=user.id,
            department_id=int(department_id),
            faculty_code=f"FAC{user.id:03d}",
            full_name=request.form.get("name"),
            designation=request.form.get("designation"),
            email=request.form.get("email")
        )

        db.session.add(faculty)
        db.session.commit()

        flash("Faculty added successfully.", "success")
        return redirect(url_for("admin.faculty"))

    faculty_list = Faculty.query.order_by(
        Faculty.full_name
    ).all()

    return render_template(
        "admin/faculty.html",
        faculty_list=faculty_list,
        departments=departments
    )

@admin_bp.route("/faculty/<int:faculty_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_faculty(faculty_id):

    faculty = Faculty.query.get_or_404(faculty_id)

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    if request.method == "POST":

    faculty.full_name = request.form.get("name")
    faculty.email = request.form.get("email")
    faculty.designation = request.form.get("designation")
    faculty.department_id = int(request.form.get("department_id"))

    # Update linked User
    faculty.user.username = request.form.get("username")
    faculty.user.email = request.form.get("email")

    password = request.form.get("password")
    if password:
        faculty.user.set_password(password)

    db.session.commit()

    flash("Faculty updated successfully.", "success")
    return redirect(url_for("admin.faculty"))

    faculty_list = Faculty.query.order_by(Faculty.full_name).all()

    return render_template(
        "admin/faculty.html",
        faculty_list=faculty_list,
        departments=departments
    )

@admin_bp.route("/faculty/<int:faculty_id>/delete", methods=["POST"])
@admin_required
def delete_faculty(faculty_id):
    faculty = Faculty.query.get_or_404(faculty_id)
    db.session.delete(faculty)
    db.session.commit()
    flash("Faculty deleted successfully.", "success")
    return redirect(url_for("admin.faculty"))


@admin_bp.route("/departments")
@admin_required
def departments():
    departments = Department.query.order_by(Department.department_name).all()
    return render_template("admin/departments.html", departments=departments)


@admin_bp.route("/departments/add", methods=["GET", "POST"])
@admin_required
def add_department():
    if request.method == "POST":
        Department(
    department_name=request.form.get("department_name"),
    department_code=request.form.get("department_code")
)
        db.session.add(department)
        db.session.commit()
        flash("Department added successfully.", "success")
        return redirect(url_for("admin.departments"))

    return render_template("admin/add_department.html")


@admin_bp.route("/departments/<int:department_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_department(department_id):
    department = Department.query.get_or_404(department_id)

    if request.method == "POST":
        department.name = request.form.get("name")
        db.session.commit()
        flash("Department updated successfully.", "success")
        return redirect(url_for("admin.departments"))

    return render_template("admin/edit_department.html", department=department)


@admin_bp.route("/departments/<int:department_id>/delete", methods=["POST"])
@admin_required
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    flash("Department deleted successfully.", "success")
    return redirect(url_for("admin.departments"))


@admin_bp.route("/courses")
@admin_required
def courses():
    courses = Course.query.order_by(Course.course_name).all()
    return render_template("admin/courses.html", courses=courses)


@admin_bp.route("/courses/add", methods=["GET", "POST"])
@admin_required
def add_course():
    departments = Department.query.order_by(Department.department_name).all()

    if request.method == "POST":
        course = Course(
            name=request.form.get("name"),
            code=request.form.get("code"),
            department_id=request.form.get("department_id"),
        )
        db.session.add(course)
        db.session.commit()
        flash("Course added successfully.", "success")
        return redirect(url_for("admin.courses"))

    return render_template("admin/add_course.html", departments=departments)


@admin_bp.route("/courses/<int:course_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    departments = Department.query.order_by(Department.department_name).all()
    if request.method == "POST":
        course.name = request.form.get("name")
        course.code = request.form.get("code")
        course.department_id = request.form.get("department_id")

        db.session.commit()
        flash("Course updated successfully.", "success")
        return redirect(url_for("admin.courses"))

    return render_template("admin/edit_course.html", course=course, departments=departments)


@admin_bp.route("/courses/<int:course_id>/delete", methods=["POST"])
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash("Course deleted successfully.", "success")
    return redirect(url_for("admin.courses"))


@admin_bp.route("/feedback")
@admin_required
def feedback():
    feedback_list = Feedback.query.order_by(Feedback.id.desc()).all()
    return render_template("admin/feedback.html", feedback_list=feedback_list)


@admin_bp.route("/feedback/<int:feedback_id>")
@admin_required
def view_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    return render_template("admin/view_feedback.html", feedback=feedback)


@admin_bp.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
@admin_required
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    flash("Feedback deleted successfully.", "success")
    return redirect(url_for("admin.feedback"))


@admin_bp.route("/reports")
@admin_required
def reports():
    data = get_dashboard_stats()
    return render_template("admin/reports.html", **data)


@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    if request.method == "POST":
        flash("Settings updated successfully.", "success")
        return redirect(url_for("admin.settings"))

    return render_template("admin/settings.html")


@admin_bp.route("/profile")
@admin_required
def profile():
    return render_template("admin/profile.html")


@admin_bp.route("/logout")
@admin_required
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))