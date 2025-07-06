from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.services.user_service import UserService
from app.models.user import User
from app.db.database import get_session
from sqlmodel import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:

    return UserService(session).get_current_user(token)
