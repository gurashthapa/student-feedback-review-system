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
    User,
    Student,
    Faculty,
    Course,
    Department,
    Feedback,
    Notification,
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

    avg_rating = db.session.query(
        func.avg(Feedback.rating)
    ).scalar() or 0

    rating_values = [
        Feedback.query.filter_by(rating=i).count()
        for i in range(1, 6)
    ]

    distribution_values = [
        Feedback.query.filter_by(status="Pending").count(),
        Feedback.query.filter_by(status="Approved").count(),
        Feedback.query.filter_by(status="Rejected").count()
    ]

    recent_feedback = (
        Feedback.query.order_by(Feedback.created_at.desc())
        .limit(10)
        .all()
    )

    # ADD THIS HERE
    unread_notifications = Notification.query.filter_by(
        is_read=False
    ).count()

    notifications = (
        Notification.query
        .order_by(Notification.created_at.desc())
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

        # ALSO ADD THESE TWO
        "unread_notifications": unread_notifications,
        "notifications": notifications,
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

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    if request.method == "POST":

        department_id = request.form.get("department_id")

        if not department_id:
            flash("Please select a department.", "danger")
            return redirect(url_for("admin.students"))

        # Check if username already exists
        if User.query.filter_by(username=request.form.get("username")).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("admin.students"))

        # Check if email already exists
        if User.query.filter_by(email=request.form.get("email")).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("admin.students"))

        # Check if student ID already exists
        if Student.query.filter_by(student_id=request.form.get("student_id")).first():
            flash("Student ID already exists.", "danger")
            return redirect(url_for("admin.students"))

        password = request.form.get("password")

        if not password:
            flash("Password is required.", "danger")
            return redirect(url_for("admin.students"))

        # Create User account
        user = User(
            username=request.form.get("username"),
            email=request.form.get("email"),
            role="student"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.flush()   # Generates user.id

        # Create Student
        student = Student(
            user_id=user.id,
            student_id=request.form.get("student_id"),
            full_name=request.form.get("full_name"),
            email=request.form.get("email"),
            department_id=int(department_id),
            phone=request.form.get("phone"),
            address=request.form.get("address"),
            gender=request.form.get("gender"),
            year=int(request.form.get("year")),
            semester=int(request.form.get("semester")),
            section=request.form.get("section")
        )

        db.session.add(student)
        db.session.commit()

        flash("Student added successfully.", "success")
        return redirect(url_for("admin.students"))

    return render_template(
        "admin/students.html",
        students=Student.query.order_by(Student.full_name).all(),
        departments=departments
    )

@admin_bp.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_student(student_id):

    student = Student.query.get_or_404(student_id)
    departments = Department.query.order_by(
        Department.department_name
    ).all()

    if request.method == "POST":

        student.student_id = request.form.get("student_id")
        student.full_name = request.form.get("full_name")
        student.email = request.form.get("email")
        student.department_id = request.form.get("department_id")
        student.semester = request.form.get("semester")

        db.session.commit()

        flash("Student updated successfully.", "success")

        return redirect(url_for("admin.students"))

    return render_template(
        "admin/edit_student.html",
        student=student,
        departments=departments
    )


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


@admin_bp.route("/faculty/add", methods=["GET", "POST"])
@admin_required
def add_faculty():

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    if request.method == "POST":

        department_id = request.form.get("department_id")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate department
        if not department_id:
            flash("Please select a department.", "danger")
            return redirect(url_for("admin.faculty"))

        # Validate username
        if not username:
            flash("Username is required.", "danger")
            return redirect(url_for("admin.faculty"))

        # Validate email
        if not email:
            flash("Email is required.", "danger")
            return redirect(url_for("admin.faculty"))

        # Validate password
        if not password:
            flash("Password is required.", "danger")
            return redirect(url_for("admin.faculty"))

        # Check duplicate username
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("admin.faculty"))

        # Check duplicate email
        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("admin.faculty"))

        # Create login account
        user = User(
            username=username,
            email=email,
            role="faculty"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.flush()   # Generates user.id

        # Create faculty record
        faculty = Faculty(
            user_id=user.id,
            department_id=int(department_id),
            faculty_code=f"FAC{user.id:03d}",
            full_name=request.form.get("name"),
            designation=request.form.get("designation"),
            email=email
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

        department_id = request.form.get("department_id")

        if not department_id:
            flash("Please select a department.", "danger")
            return redirect(url_for("admin.faculty"))

        # Check if another user already has this username
        username = request.form.get("username")
        existing_user = User.query.filter(
            User.username == username,
            User.id != faculty.user_id
        ).first()

        if existing_user:
            flash("Username already exists.", "danger")
            return redirect(url_for("admin.faculty"))

        # Check if another user already has this email
        email = request.form.get("email")
        existing_email = User.query.filter(
            User.email == email,
            User.id != faculty.user_id
        ).first()

        if existing_email:
            flash("Email already exists.", "danger")
            return redirect(url_for("admin.faculty"))

        # Update Faculty table
        faculty.full_name = request.form.get("name")
        faculty.email = email
        faculty.designation = request.form.get("designation")
        faculty.department_id = int(department_id)

        # Update User table
        faculty.user.username = username
        faculty.user.email = email

        password = request.form.get("password")
        if password:
            faculty.user.set_password(password)

        db.session.commit()

        flash("Faculty updated successfully.", "success")
        return redirect(url_for("admin.faculty"))

    faculty_list = Faculty.query.order_by(
        Faculty.full_name
    ).all()

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

        department_name = request.form.get("department_name")
        department_code = request.form.get("department_code")

        # Validation
        if not department_name:
            flash("Department name is required.", "danger")
            return redirect(url_for("admin.add_department"))

        if not department_code:
            flash("Department code is required.", "danger")
            return redirect(url_for("admin.add_department"))

        # Check duplicate department name
        if Department.query.filter_by(department_name=department_name).first():
            flash("Department name already exists.", "danger")
            return redirect(url_for("admin.add_department"))

        # Check duplicate department code
        if Department.query.filter_by(department_code=department_code).first():
            flash("Department code already exists.", "danger")
            return redirect(url_for("admin.add_department"))

        department = Department(
            department_name=department_name,
            department_code=department_code,
            description=request.form.get("description"),
            hod_name=request.form.get("hod_name"),
            office_location=request.form.get("office_location"),
            contact_email=request.form.get("contact_email"),
            contact_phone=request.form.get("contact_phone"),
            status=request.form.get("status") or "Active"
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

        department_name = request.form.get("department_name")
        department_code = request.form.get("department_code")

        # Validation
        if not department_name:
            flash("Department name is required.", "danger")
            return redirect(
                url_for("admin.edit_department", department_id=department.id)
            )

        if not department_code:
            flash("Department code is required.", "danger")
            return redirect(
                url_for("admin.edit_department", department_id=department.id)
            )

        # Check duplicate department name
        existing_name = Department.query.filter(
            Department.department_name == department_name,
            Department.id != department.id
        ).first()

        if existing_name:
            flash("Department name already exists.", "danger")
            return redirect(
                url_for("admin.edit_department", department_id=department.id)
            )

        # Check duplicate department code
        existing_code = Department.query.filter(
            Department.department_code == department_code,
            Department.id != department.id
        ).first()

        if existing_code:
            flash("Department code already exists.", "danger")
            return redirect(
                url_for("admin.edit_department", department_id=department.id)
            )

        # Update department
        department.department_name = department_name
        department.department_code = department_code
        department.description = request.form.get("description")
        department.hod_name = request.form.get("hod_name")
        department.office_location = request.form.get("office_location")
        department.contact_email = request.form.get("contact_email")
        department.contact_phone = request.form.get("contact_phone")
        department.status = request.form.get("status")

        db.session.commit()

        flash("Department updated successfully.", "success")
        return redirect(url_for("admin.departments"))

    return render_template(
        "admin/edit_department.html",
        department=department
    )
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
    departments = Department.query.order_by(Department.department_name).all()
    faculty_list = Faculty.query.order_by(Faculty.full_name).all()

    return render_template(
        "admin/courses.html",
        courses=courses,
        departments=departments,
        faculty_list=faculty_list
    )

@admin_bp.route("/courses/add", methods=["GET", "POST"])
@admin_required
def add_course():
    departments = Department.query.order_by(Department.department_name).all()

    if request.method == "POST":
        course = Course(
    course_name=request.form.get("course_name"),
    course_code=request.form.get("course_code"),
    department_id=request.form.get("department_id")
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

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    faculty_list = Faculty.query.order_by(
        Faculty.full_name
    ).all()

    if request.method == "POST":

        course_name = request.form.get("course_name")
        course_code = request.form.get("course_code")

        if not course_name:
            flash("Course name is required.", "danger")
            return redirect(
                url_for("admin.edit_course", course_id=course.id)
            )

        if not course_code:
            flash("Course code is required.", "danger")
            return redirect(
                url_for("admin.edit_course", course_id=course.id)
            )

        # Check duplicate course code
        existing_course = Course.query.filter(
            Course.course_code == course_code,
            Course.id != course.id
        ).first()

        if existing_course:
            flash("Course code already exists.", "danger")
            return redirect(
                url_for("admin.edit_course", course_id=course.id)
            )

        # Update course
        course.course_name = course_name
        course.course_code = course_code
        course.department_id = int(request.form.get("department_id"))
        course.faculty_id = int(request.form.get("faculty_id"))
        course.semester = int(request.form.get("semester"))
        course.credit = int(request.form.get("credit"))
        course.description = request.form.get("description")
        course.status = request.form.get("status")

        db.session.commit()

        flash("Course updated successfully.", "success")
        return redirect(url_for("admin.courses"))

    return render_template(
        "admin/edit_course.html",
        course=course,
        departments=departments,
        faculty_list=faculty_list
    )
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

    feedback_list = Feedback.query.order_by(
        Feedback.id.desc()
    ).all()

    return render_template(
        "admin/feedback.html",
        feedback_list=feedback_list
    )

@admin_bp.route("/feedback/<int:feedback_id>/approve", methods=["POST"])
@admin_required
def approve_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)

    feedback.status = "Approved"

    notification = Notification.query.filter_by(
        feedback_id=feedback.id
    ).first()

    if notification:
        db.session.delete(notification)

    db.session.commit()

    flash("Feedback approved successfully.", "success")

    return redirect(url_for("admin.feedback"))



@admin_bp.route("/feedback/<int:feedback_id>/reject", methods=["POST"])
@admin_required
def reject_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)

    feedback.status = "Rejected"

    notification = Notification.query.filter_by(
        feedback_id=feedback.id
    ).first()

    if notification:
        db.session.delete(notification)

    db.session.commit()

    flash("Feedback rejected successfully.", "warning")

    return redirect(url_for("admin.feedback"))


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

@admin_bp.route("/notifications/read")
@admin_required
def read_notifications():

    Notification.query.update(
        {
            Notification.is_read: True
        }
    )

    db.session.commit()

    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/logout")
@admin_required
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))