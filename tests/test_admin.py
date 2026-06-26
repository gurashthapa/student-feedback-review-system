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
            db.drop_all()


def test_register(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "role": "student"
    })
    assert response.status_code in (200, 201)


def test_login(client):
    client.post("/auth/register", json={
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "password123",
        "role": "student"
    })

    response = client.post("/auth/login", json={
        "email": "test2@example.com",
        "password": "password123"
    })
    assert response.status_code == 200


def test_invalid_login(client):
    response = client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpass"
    })
    assert response.status_code in (400, 401)