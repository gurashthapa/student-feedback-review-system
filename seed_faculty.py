from datetime import date

from app import create_app, db
from app.models.user import User
from app.models.faculty import Faculty
from app.models.department import Department

app = create_app()

with app.app_context():

    department = Department.query.first()

    if department is None:
        print("No department found.")
        exit()

    existing_user = User.query.filter_by(
        email="faculty@test.com"
    ).first()

    if existing_user:
        print("Faculty user already exists.")
        exit()

    user = User(
        username="faculty",
        email="faculty@test.com",
        role="faculty",
        is_active=True
    )

    user.set_password("1234")

    db.session.add(user)
    db.session.commit()

    faculty = Faculty(
        user_id=user.id,
        department_id=department.id,
        faculty_code="FAC001",
        full_name="John Smith",
        designation="Assistant Professor",
        qualification="MSc Computer Science",
        specialization="Database Systems",
        email="faculty@test.com",
        phone="9800000000",
        address="Kathmandu",
        gender="Male",
        joining_date=date.today(),
        status="Active"
    )

    db.session.add(faculty)
    db.session.commit()

    print("Faculty Created Successfully!")