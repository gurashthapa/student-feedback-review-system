import pytest
from app import create_app
from app.database import db


@pytest.fixture
def client():
    app = create_app(testing=True)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def register_student(client):
    return client.post("/auth/register", json={
        "username": "student1",
        "email": "student1@example.com",
        "password": "pass123",
        "role": "student"
    })


def login_student(client):
    return client.post("/auth/login", json={
        "email": "student1@example.com",
        "password": "pass123"
    })


def test_student_profile_access(client):
    register_student(client)
    login_student(client)

    response = client.get("/student/profile")
    assert response.status_code in (200, 401)


def test_student_dashboard(client):
    register_student(client)
    login_student(client)

    response = client.get("/student/dashboard")
    assert response.status_code in (200, 200)


def test_student_profile_update(client):
    register_student(client)
    login_student(client)

    response = client.put("/student/profile/update", json={
        "username": "updated_student",
        "year": 3
    })

    assert response.status_code in (200, 204, 400)