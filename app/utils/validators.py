import re
from app.utils.helpers import is_valid_email


def validate_user(data):
    """
    Validate user registration/login data
    """
    errors = {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not name:
        errors["name"] = "Name is required"
    elif len(name) < 3:
        errors["name"] = "Name must be at least 3 characters"

    if not email:
        errors["email"] = "Email is required"
    elif not is_valid_email(email):
        errors["email"] = "Invalid email format"

    if not password:
        errors["password"] = "Password is required"
    elif len(password) < 6:
        errors["password"] = "Password must be at least 6 characters"

    return errors

def validate_student(data):
    errors = {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    department = data.get("department", "").strip()
    semester = data.get("semester", "")

    if not name:
        errors["name"] = "Student name is required"

    if not email:
        errors["email"] = "Email is required"
    elif not is_valid_email(email):
        errors["email"] = "Invalid email format"

    if not department:
        errors["department"] = "Department is required"

    if not semester:
        errors["semester"] = "Semester is required"
    else:
        try:
            semester = int(semester)
            if semester < 1 or semester > 8:
                errors["semester"] = "Semester must be between 1 and 8"
        except:
            errors["semester"] = "Semester must be a number"

    return errors

def validate_faculty(data):
    errors = {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    department = data.get("department", "").strip()
    designation = data.get("designation", "").strip()

    if not name:
        errors["name"] = "Faculty name is required"

    if not email:
        errors["email"] = "Email is required"
    elif not is_valid_email(email):
        errors["email"] = "Invalid email format"

    if not department:
        errors["department"] = "Department is required"

    if not designation:
        errors["designation"] = "Designation is required"

    return errors


def validate_course(data):
    errors = {}

    name = data.get("name", "").strip()
    department = data.get("department", "").strip()
    credits = data.get("credits", "")

    if not name:
        errors["name"] = "Course name is required"

    if not department:
        errors["department"] = "Department is required"

    if not credits:
        errors["credits"] = "Credits are required"
    else:
        try:
            credits = int(credits)
            if credits <= 0:
                errors["credits"] = "Credits must be greater than 0"
        except:
            errors["credits"] = "Credits must be a number"

    return errors

def validate_feedback(data):
    errors = {}

    rating = data.get("rating", "")
    comment = data.get("comment", "").strip()

    if not rating:
        errors["rating"] = "Rating is required"
    else:
        try:
            rating = float(rating)
            if rating < 1 or rating > 5:
                errors["rating"] = "Rating must be between 1 and 5"
        except:
            errors["rating"] = "Rating must be a number"

    if not comment:
        errors["comment"] = "Comment is required"
    elif len(comment) < 10:
        errors["comment"] = "Comment must be at least 10 characters"

    return errors


def validate_login(data):
    errors = {}

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email:
        errors["email"] = "Email is required"
    elif not is_valid_email(email):
        errors["email"] = "Invalid email format"

    if not password:
        errors["password"] = "Password is required"

    return errors


def validate_password_reset(data):
    errors = {}

    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")

    if not password:
        errors["password"] = "Password is required"
    elif len(password) < 6:
        errors["password"] = "Password must be at least 6 characters"

    if password != confirm_password:
        errors["confirm_password"] = "Passwords do not match"

    return errors


def validate_text(field_name, value, min_length=1, max_length=255):
    errors = {}

    value = value.strip() if value else ""

    if not value:
        errors[field_name] = f"{field_name} is required"
    elif len(value) < min_length:
        errors[field_name] = f"{field_name} must be at least {min_length} characters"
    elif len(value) > max_length:
        errors[field_name] = f"{field_name} must not exceed {max_length} characters"

    return errors