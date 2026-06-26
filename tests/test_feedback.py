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


def register_user(client, username, email, password, role):
    return client.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password,
        "role": role
    })


def login_user(client, email, password):
    return client.post("/auth/login", json={
        "email": email,
        "password": password
    })


def test_submit_feedback(client):
    register_user(client, "student1", "s1@example.com", "pass123", "student")
    register_user(client, "faculty1", "f1@example.com", "pass123", "faculty")

    login_user(client, "s1@example.com", "pass123")

    response = client.post("/feedback/create", json={
        "student_id": 1,
        "faculty_id": 1,
        "course_id": 1,
        "rating": 5,
        "comment": "Great teaching"
    })

    assert response.status_code in (200, 201)


def test_get_feedback(client):
    response = client.get("/feedback/all")
    assert response.status_code == 200


def test_invalid_feedback_rating(client):
    register_user(client, "student2", "s2@example.com", "pass123", "student")
    register_user(client, "faculty2", "f2@example.com", "pass123", "faculty")

    login_user(client, "s2@example.com", "pass123")

    response = client.post("/feedback/create", json={
        "student_id": 1,
        "faculty_id": 1,
        "course_id": 1,
        "rating": 10,
        "comment": "Invalid rating test"
    })

    assert response.status_code in (400, 422)