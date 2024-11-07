from tests.db_test import client
from app import schemas

def test_root(client):
    response = client.get("/")
    print(response.json())
    assert response.status_code == 200
    assert response.json().get("message") == "Learning python API and Pushing the code to Ubuntu server"

def test_create_user(client):
    response = client.post("/users/", json={"email": "hello123456@example.com", "password": "123456"})
    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "hello123456@example.com"

# def test_login_user(client):
#     response = client.post("/login", data={"email": "hello123456@example.com", "password": "123456"})
#     assert response.status_code == 200

