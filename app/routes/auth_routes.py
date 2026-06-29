from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app import db
from app.models.user import User
from app.models.student import Student
from app.models.department import Department


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


def parse_date(dob):
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(dob, fmt).date()
        except ValueError:
            pass
    raise ValueError("Invalid date format")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        print("========== LOGIN DEBUG ==========")
        print("Email entered:", email)
        print("User found:", user)

        if user:
            print("User ID:", user.id)
            print("Role:", user.role)
            print("Active:", user.is_active)
            print("Password correct:", user.check_password(password))

        print("=================================")

        if user is None:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        if not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        if not user.is_active:
            flash("Your account is disabled.", "danger")
            return redirect(url_for("auth.login"))

        session.clear()

        session["user_id"] = user.id
        session["role"] = user.role
        session["username"] = user.username

        flash("Login successful.", "success")

        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        elif user.role == "faculty":
            return redirect(url_for("faculty.statistics"))

        elif user.role == "student":
            return redirect(url_for("student.dashboard"))

        flash("Invalid user role.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    departments = Department.query.all()

    if request.method == "POST":

        full_name = request.form.get("full_name")
        student_id = request.form.get("student_id")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        department_id = request.form.get("department_id")
        year = request.form.get("year")
        semester = request.form.get("semester")
        section = request.form.get("section")
        phone = request.form.get("phone")
        gender = request.form.get("gender")
        address = request.form.get("address")
        dob = request.form.get("date_of_birth")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        if not department_id:
            flash("Please select a department.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))

        existing_student = Student.query.filter_by(student_id=student_id).first()
        if existing_student:
            flash("Student ID already exists.", "danger")
            return redirect(url_for("auth.register"))

        try:

            user = User(
                username=student_id,
                email=email,
                role="student",
                is_active=True
            )

            user.set_password(password)

            db.session.add(user)
            db.session.flush()

            dob_date = parse_date(dob) if dob else None

            student = Student(
                user_id=user.id,
                department_id=int(department_id),
                student_id=student_id,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                gender=gender,
                date_of_birth=dob_date,
                year=int(year),
                semester=int(semester),
                section=section
            )

            db.session.add(student)
            db.session.commit()

            flash("Registration successful. Please login.", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            db.session.rollback()
            print(e)
            flash(f"Registration failed: {e}", "danger")
            return redirect(url_for("auth.register"))

    return render_template(
        "auth/register.html",
        departments=departments
    )


@auth_bp.route("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_password.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))