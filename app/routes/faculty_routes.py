from flask import Blueprint, render_template

faculty_bp = Blueprint(
    "faculty",
    __name__,
    url_prefix="/faculty"
)

@faculty_bp.route("/dashboard")
def dashboard():
    return render_template("faculty/dashboard.html")