from app import create_app
from app.models.student import Student
from app.models.course import Course

app = create_app()

with app.app_context():
    student = Student.query.filter_by(email="gurash19@gmail.com").first()

    print("Student:", student.full_name)
    print("Department:", student.department_id)
    print("Semester:", student.semester)

    courses = Course.query.filter_by(
        department_id=student.department_id,
        semester=student.semester,
        status="Active"
    ).all()

    print("Courses found:")
    for c in courses:
        print(c.course_name)