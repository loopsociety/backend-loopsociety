from typing import Optional
from sqlmodel import Session, select
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.models.user import User
from app.utils.auth import create_token, get_token_hash
from app.schemas.auth import TokenResponse

from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.db.database import get_session
from app.models.user_session import UserSession
from datetime import timedelta, datetime
import hashlib


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
    if not email or not password:
        raise HTTPException(
            status_code=400, detail="Email and password are required")

    query = select(User).where(
        (User.email == email)
    )
    user = session.exec(query).first()
    if not user or not verify_password(password, user.password_hash):
        return HTTPException(status_code=401, detail="Invalid credentials")

    return user


def login_user(
    user: User, request: Request, session: Session
):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_token, _ = create_token({"sub": str(user.id)}, access_token_expires)
    refresh_token, exp = create_token(
        {"sub": str(user.id)}, refresh_token_expires)

    refresh_token_hash = get_token_hash(refresh_token)

    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("User-Agent", "unknown")

    session_entry = UserSession(
        user_id=user.id,
        refresh_token_hash=refresh_token_hash,
        ip_address=ip_address,
        user_agent=user_agent,
        is_active=True,
        created_at=datetime.utcnow(),
        expires_at=exp,
    )
    session.add(session_entry)
    session.commit()
    session.refresh(session_entry)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_token(
    refresh_token: str, session
) -> TokenResponse:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    refresh_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

    db_session = session.exec(
        select(UserSession)
        .where(UserSession.user_id == user_id)
        .where(UserSession.refresh_token_hash == refresh_hash)
        .where(UserSession.is_active == True)
    ).first()

    if not db_session:
        raise HTTPException(status_code=401, detail="Invalid session")

    access_token, _ = create_token(
        {"sub": str(user_id)}, timedelta(minutes=15))
    new_refresh_token, _ = create_token(
        {"sub": str(user_id)}, timedelta(days=7))

    db_session.refresh_token_hash = hashlib.sha256(
        new_refresh_token.encode()).hexdigest()
    session.add(db_session)
    session.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token
    )


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
        raise HTTPException(status_code=404, detail="User not found")

    return user
