from flask import Blueprint

feedback_bp = Blueprint(
    "feedback",
    __name__,
    url_prefix="/feedback"
)

@feedback_bp.route("/")
def index():
    return "Feedback Module"