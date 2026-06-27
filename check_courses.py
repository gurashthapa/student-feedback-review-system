from app import create_app
from app.models.course import Course

app = create_app()

with app.app_context():
    courses = Course.query.all()

    print("=" * 50)
    print("Total Courses:", len(courses))
    print("=" * 50)

    if not courses:
        print("No courses found in the database.")
    else:
        for c in courses:
            print(
                f"ID={c.id}, "
                f"Name={c.course_name}, "
                f"Department={c.department_id}, "
                f"Semester={c.semester}, "
                f"Faculty={c.faculty_id}, "
                f"Status={c.status}"
            )