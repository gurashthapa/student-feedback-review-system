from flask import session, redirect, url_for
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    """
    Convert plain password into a secure hash
    """
    return generate_password_hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    """
    Check if plain password matches hashed password
    """
    return check_password_hash(hashed_password, password)

def get_current_user():
    """
    Return logged-in user from session
    """
    return session.get("user")


def get_user_role():
    """
    Return role of current user (student/faculty/admin)
    """
    user = session.get("user")
    if user:
        return user.get("role")
    return None


def is_logged_in():
    """
    Check if user is logged in
    """
    return "user" in session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    """
    Restrict access based on user role
    Example: @role_required('admin')
    """
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get("user")

            if not user:
                return redirect(url_for("auth.login"))

            if user.get("role") != role:
                return redirect(url_for("auth.unauthorized"))

            return f(*args, **kwargs)

        return decorated_function

    return wrapper


def roles_required(roles):
    """
    Allow multiple roles access
    Example: @roles_required(['admin','faculty'])
    """
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get("user")

            if not user:
                return redirect(url_for("auth.login"))

            if user.get("role") not in roles:
                return redirect(url_for("auth.unauthorized"))

            return f(*args, **kwargs)

        return decorated_function

    return wrapper