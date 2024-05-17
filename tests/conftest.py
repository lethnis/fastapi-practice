import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base
from app.config import settings
from app.routers import oauth2
from app.models import PostTable


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@test.com", "password": "test"}
    new_user = client.post("/users/", json=user_data)
    assert new_user.status_code == 201
    new_user = new_user.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@test.com", "password": "test2"}
    new_user = client.post("/users/", json=user_data)
    assert new_user.status_code == 201
    new_user = new_user.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {"title": "test title", "content": "test content", "user_id": test_user["id"]},
        {"title": "test title 2", "content": "test content 2", "user_id": test_user["id"]},
        {"title": "test title 3", "content": "test content 3", "user_id": test_user["id"]},
        {"title": "test by user 2", "content": "test content by user 2", "user_id": test_user2["id"]},
    ]

    session.add_all([PostTable(**i) for i in posts_data])

    session.commit()

    return session.query(PostTable).all()
