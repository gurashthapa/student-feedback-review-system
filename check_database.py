from app import create_app
from app.models.department import Department
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.course import Course

app = create_app()

with app.app_context():
    print("Departments :", Department.query.count())
    print("Faculty     :", Faculty.query.count())
    print("Students    :", Student.query.count())
    print("Courses     :", Course.query.count())