from functools import wraps
from flask import session, redirect, url_for, flash

def current_user():
    return session.get("user")


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()

        if not user:
            flash("Please login first", "warning")
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return wrapper


def role_required(role):
    """
    Example:
    @role_required('admin')
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = current_user()

            if not user:
                flash("Login required", "danger")
                return redirect(url_for("auth.login"))

            if user.get("role") != role:
                flash("Access denied: Admins only", "danger")
                return redirect(url_for("auth.unauthorized"))

            return f(*args, **kwargs)

        return wrapper
    return decorator

def roles_required(roles):
    """
    Example:
    @roles_required(['admin', 'faculty'])
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = current_user()

            if not user:
                flash("Login required", "danger")
                return redirect(url_for("auth.login"))

            if user.get("role") not in roles:
                flash("You do not have permission to access this page", "danger")
                return redirect(url_for("auth.unauthorized"))

            return f(*args, **kwargs)

        return wrapper
    return decorator

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()

        if not user:
            flash("Login required", "danger")
            return redirect(url_for("auth.login"))

        if user.get("role") != "admin":
            flash("Admin access only", "danger")
            return redirect(url_for("auth.unauthorized"))

        return f(*args, **kwargs)

    return wrapper


def faculty_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()

        if not user:
            flash("Login required", "danger")
            return redirect(url_for("auth.login"))

        if user.get("role") != "faculty":
            flash("Faculty access only", "danger")
            return redirect(url_for("auth.unauthorized"))

        return f(*args, **kwargs)

    return wrapper


def student_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()

        if not user:
            flash("Login required", "danger")
            return redirect(url_for("auth.login"))

        if user.get("role") != "student":
            flash("Student access only", "danger")
            return redirect(url_for("auth.unauthorized"))

        return f(*args, **kwargs)

    return wrapper


def email_verified_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()

        if not user:
            flash("Login required", "danger")
            return redirect(url_for("auth.login"))

        if not user.get("email_verified", False):
            flash("Please verify your email first", "warning")
            return redirect(url_for("auth.verify_email"))

        return f(*args, **kwargs)

    return wrapper


def active_account_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()

        if not user:
            flash("Login required", "danger")
            return redirect(url_for("auth.login"))

        if not user.get("is_active", True):
            flash("Your account is deactivated", "danger")
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return wrapper