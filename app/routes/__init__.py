from .auth_routes import auth_bp
from .student_routes import student_bp
from .faculty_routes import faculty_bp
from .admin_routes import admin_bp
from .feedback_routes import feedback_bp
from .department_routes import department_bp
from .course_routes import course_bp
from .profile_routes import profile_bp
from .report_routes import report_bp

all_blueprints = [
    auth_bp,
    student_bp,
    faculty_bp,
    admin_bp,
    feedback_bp,
    department_bp,
    course_bp,
    profile_bp,
    report_bp
]