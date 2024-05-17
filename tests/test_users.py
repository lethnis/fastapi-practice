import pytest
from jose import jwt

from app.schemas import UserResponse, Token
from app.config import settings


def test_root(client):
    response = client.get("/")
    assert response.json() == {"message": "Hello World!"}
    assert response.status_code == 200


def test_create_user(test_user):
    assert test_user["id"] is not None
    assert test_user["email"] is not None
    assert test_user["created_at"] is not None


def test_login(client, test_user):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200

    token = Token(**response.json())
    assert token.access_token is not None
    assert token.token_type is not None
    assert token.token_type == "bearer"

    payload = jwt.decode(token.access_token, settings.secret_key, settings.algorithm)
    assert payload.get("user_id") == test_user["id"]


@pytest.mark.parametrize(
    "email, password, status_code, detail",
    [
        ("test@test.com", "wrong", 403, "Wrong password"),
        ("wrong@wrong.com", "test", 403, "User with this email not found"),
        (None, "test", 422, [{"input": None, "loc": ["body", "username"], "msg": "Field required", "type": "missing"}]),
        (
            "test@test.com",
            None,
            422,
            [{"input": None, "loc": ["body", "password"], "msg": "Field required", "type": "missing"}],
        ),
    ],
)
def test_incorrect_password(test_user, client, email, password, status_code, detail):
    response = client.post("/login", data={"username": email, "password": password})

    assert response.status_code == status_code
    assert response.json().get("detail") == detail


# def test_incorrect_password(test_user, client):
#     response = client.post("/login", data={"username": "test@test.com", "password": "wrong"})

#     assert response.status_code == 403
#     assert response.json().get("detail") == "Wrong password"


# def test_incorrect_username(test_user, client):
#     response = client.post("/login", data={"username": "wrong@wrong.com", "password": test_user["password"]})

#     assert response.status_code == 403
#     assert response.json().get("detail") == "User with this email not found"
