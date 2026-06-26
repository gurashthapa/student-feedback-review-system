from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

# Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print(email, password)

        # TODO: Check database
        return redirect(url_for("student.dashboard"))

    return render_template("auth/login.html")


# Register
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        print(name, email, password, role)

        # TODO: Save to database
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# Forgot Password
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")

        print(email)

        # TODO: Send reset email
        return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html")