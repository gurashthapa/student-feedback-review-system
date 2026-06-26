from flask import Blueprint

profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)

@profile_bp.route("/")
def index():
    return "Profile Module"