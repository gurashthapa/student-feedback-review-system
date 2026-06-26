from flask import Blueprint, render_template, request, redirect, url_for

student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)

@student_bp.route("/dashboard")
def dashboard():
    return render_template(
        "student/dashboard.html",
        total_feedback=0,
        avg_rating=0,
        total_courses=0,
        total_faculty=0,
        recent_feedback=[]
    )


# Feedback
@student_bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        faculty_id = request.form.get("faculty_id")
        course_id = request.form.get("course_id")
        rating = request.form.get("rating")
        comment = request.form.get("comment")

        print(faculty_id, course_id, rating, comment)

        return redirect(url_for("student.dashboard"))

    return render_template(
        "student/feedback.html",
        faculty=[],
        courses=[]
    )


@student_bp.route("/history")
def history():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT
        f.name AS faculty_name,
        c.course_name,
        fb.rating,
        fb.comment,
        fb.created_at
    FROM feedback fb
    JOIN faculty f ON fb.faculty_id = f.id
    JOIN courses c ON fb.course_id = c.id
    ORDER BY fb.created_at DESC
    """)

    feedbacks = cursor.fetchall()

    return render_template(
        "student/history.html",
        feedbacks=feedbacks
    )

# Profile
@student_bp.route("/profile", methods=["GET", "POST"])
def profile():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        department = request.form.get("department")
        semester = request.form.get("semester")
        password = request.form.get("password")

        print(name, email, department, semester, password)

        return redirect(url_for("student.profile"))

    user = {
        "name": "Student",
        "email": "student@example.com",
        "department": "Computer Science",
        "semester": 1,
        "role": "student"
    }

    return render_template("student/profile.html", user=user)
