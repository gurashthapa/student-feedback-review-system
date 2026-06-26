from flask import Blueprint

course_bp = Blueprint(
    "course",
    __name__,
    url_prefix="/course"
)

@course_bp.route("/")
def index():
    return "Course Module"