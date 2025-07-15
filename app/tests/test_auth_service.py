import pytest
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine
from app.services.auth_service import AuthService
from app.models.user import User
from sqlmodel import select


@pytest.fixture
def auth_service(service_factory):
    return service_factory(AuthService)


def test_register_user(auth_service, session):
    result = auth_service.register_user(
        email="test@example.com",
        username="testuser",
        password="testpassword",
    )
    assert result["username"] == "testuser"
    assert result["email"] == "test@example.com"
    user = session.exec(
        select(User).where(User.username == "testuser")
    ).first()
    assert user is not None
    assert auth_service.verify_password("testpassword", user.password_hash)


def test_register_user_duplicate(auth_service):
    auth_service.register_user("a@b.com", "user1", "pass")
    with pytest.raises(HTTPException) as exc:
        auth_service.register_user("a@b.com", "user1", "pass")
    assert exc.value.status_code == 400


def test_authenticate_user_success(auth_service):
    auth_service.register_user("b@c.com", "user2", "pass2")
    user = auth_service.authenticate_user("b@c.com", "pass2")
    assert user.username == "user2"


def test_authenticate_user_invalid(auth_service):
    auth_service.register_user("c@d.com", "user3", "pass3")
    with pytest.raises(HTTPException) as exc:
        auth_service.authenticate_user("c@d.com", "wrongpass")
    assert exc.value.status_code == 401


def test_login_and_refresh(auth_service):
    auth_service.register_user("d@e.com", "user4", "pass4")
    user = auth_service.authenticate_user("d@e.com", "pass4")

    class DummyRequest:
        client = type("client", (), {"host": "127.0.0.1"})
        headers = {"User-Agent": "pytest"}

    request = DummyRequest()
    # Login
    tokens = auth_service.login_user(user, request)
    assert tokens.access_token
    assert tokens.refresh_token


def test_logout(auth_service):
    auth_service.register_user("e@f.com", "user5", "pass5")
    user = auth_service.authenticate_user("e@f.com", "pass5")

    class DummyRequest:
        client = type("client", (), {"host": "127.0.0.1"})
        headers = {"User-Agent": "pytest"}

    request = DummyRequest()
    tokens = auth_service.login_user(user, request)
    result = auth_service.logout_user(tokens.refresh_token, user)
    assert result["message"] == "Successfully logged out."
    # Try to refresh after logout
    with pytest.raises(HTTPException) as exc:
        auth_service.refresh_token(tokens.refresh_token)
    assert exc.value.status_code == 401
