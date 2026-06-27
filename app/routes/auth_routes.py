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

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # Debug prints
        print("Email entered:", email)
        print("User found:", user)

        if user:
            print("Role:", user.role)
            print("Password valid:", user.check_password(password))

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

    flash(
        "Registration is disabled. Please contact the administrator.",
        "warning"
    )

    return redirect(url_for("auth.login"))


@auth_bp.route("/forgot-password")
def forgot_password():

    return render_template("auth/forgot_password.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))