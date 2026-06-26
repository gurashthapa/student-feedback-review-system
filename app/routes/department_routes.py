from flask import Blueprint

department_bp = Blueprint(
    "department",
    __name__,
    url_prefix="/department"
)

@department_bp.route("/")
def index():
    return "Department Module"