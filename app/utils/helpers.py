import re
import uuid
import random
import string
from datetime import datetime


def generate_id(prefix="ID"):
    """
    Generate a unique ID with prefix
    Example: STU-8F3K2L9
    """
    unique_part = str(uuid.uuid4())[:8].upper()
    return f"{prefix}-{unique_part}"

def random_string(length=8):
    """
    Generate random alphanumeric string
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def is_valid_email(email):
    """
    Validate email format
    """
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None


def format_date(date_obj):
    """
    Convert datetime to readable format
    """
    if not date_obj:
        return ""

    return date_obj.strftime("%d-%m-%Y %H:%M:%S")


def current_timestamp():
    """
    Return current datetime
    """
    return datetime.now()


def truncate_text(text, length=100):
    """
    Shorten long text for table display
    """
    if not text:
        return ""

    if len(text) <= length:
        return text

    return text[:length] + "..."

def check_password_strength(password):
    """
    Return password strength level
    """
    score = 0

    if len(password) >= 6:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[@$!%*?&]", password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score == 3:
        return "Medium"
    else:
        return "Strong"

def slugify(text):
    """
    Convert text into URL-friendly slug
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def calculate_average(values):
    """
    Calculate average from list
    """
    if not values:
        return 0

    return sum(values) / len(values)


def rating_to_text(rating):
    """
    Convert numeric rating to text
    """
    if rating >= 4.5:
        return "Excellent"
    elif rating >= 3.5:
        return "Good"
    elif rating >= 2.5:
        return "Average"
    elif rating >= 1.5:
        return "Poor"
    else:
        return "Very Poor"


def safe_string(text):
    """
    Basic sanitization
    """
    if not text:
        return ""

    return (
        text.replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
    )


def calculate_percentage(part, total):
    """
    Calculate percentage safely
    """
    if total == 0:
        return 0

    return round((part / total) * 100, 2)