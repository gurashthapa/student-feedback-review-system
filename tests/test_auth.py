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


def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "student1",
        "email": "student1@example.com",
        "password": "pass123",
        "role": "student"
    })
    assert response.status_code in [200, 201]


def test_login_user(client):
    client.post("/auth/register", json={
        "username": "faculty1",
        "email": "faculty1@example.com",
        "password": "pass123",
        "role": "faculty"
    })

    response = client.post("/auth/login", json={
        "email": "faculty1@example.com",
        "password": "pass123"
    })
    assert response.status_code == 200


def test_login_invalid(client):
    response = client.post("/auth/login", json={
        "email": "notfound@example.com",
        "password": "wrongpass"
    })
    assert response.status_code in [400, 401, 404]