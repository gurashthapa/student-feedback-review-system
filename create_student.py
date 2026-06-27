from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Check if the user already exists
    existing = User.query.filter_by(email="gurash19@gmail.com").first()

    if existing:
        print("User already exists!")
    else:
        user = User(
            username="gurash",
            email="gurash19@gmail.com",
            role="student",
            is_active=True
        )

        user.set_password("gurash123")

        db.session.add(user)
        db.session.commit()

        print("Student user created successfully!")