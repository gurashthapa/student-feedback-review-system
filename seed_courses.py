from app import create_app, db
from app.models.course import Course
from app.models.department import Department
from app.models.faculty import Faculty

app = create_app()

with app.app_context():

    department = Department.query.first()
    faculty = Faculty.query.first()

    if department is None:
        print("No department found.")
        exit()

    if faculty is None:
        print("No faculty found.")
        exit()

    course = Course(
        course_name="Database Management System",
        course_code="CS301",
        department_id=department.id,
        faculty_id=faculty.id,
        semester=1,
        credit=3,
        description="Database Course",
        status="Active"
    )

    db.session.add(course)
    db.session.commit()

    print("Course Added Successfully!")