from typing import Optional
from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.models.user import User
from app.utils.auth import create_token
from app.schemas.auth import TokenResponse

from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM
from app.db.database import get_session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def register_user(
    email: str, username: str, password: str, session: Session
) -> Optional[User]:
    existing = session.exec(select(User).where(
        User.email == email or User.username == username)).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Email or Username already registered")

    hashed = hash_password(password)
    new_user = User(username=username,
                    email=email, password_hash=hashed)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

def authenticate_user(
    email: str, password: str, session: Session
) -> Optional[TokenResponse]:
    query = select(User).where(
        (User.email == email)
    )
    user = session.exec(query).first()
    if not user or not verify_password(password, user.password_hash):
        return HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": create_token({"sub": str(user.id)}), "token_type": "bearer"}


def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
) -> Optional[User]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.exec(select(User).where(User.id == int(user_id))).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    return user
