from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Request
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.models.user import User
from app.models.user_session import UserSession
from app.schemas.auth import TokenResponse
from app.utils.auth import create_token, get_token_hash
from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)


class AuthService:
    def __init__(self, session: Session):
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # ---------- User Authentication ----------
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def register_user(self, email: str, username: str, password: str) -> dict:
        user_exists = self.session.exec(
            select(User).where((User.email == email)
                               | (User.username == username))
        ).first()

        if user_exists:
            raise HTTPException(
                400, detail="Email or username already exists.")

        user = User(
            email=email,
            username=username,
            password_hash=self.hash_password(password)
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return {"id": user.id, "username": user.username, "email": user.email}

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.session.exec(
            select(User).where(User.email == email)).first()

        if not user or not self.verify_password(password, user.password_hash):
            raise HTTPException(401, detail="Invalid credentials")

        return user

    # ---------- Token Handling ----------
    def _generate_tokens(self, user_id: int) -> tuple[str, str, datetime]:
        access_token, _ = create_token(
            {"sub": str(user_id)},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token, refresh_exp = create_token(
            {"sub": str(user_id)},
            timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        return access_token, refresh_token, refresh_exp

    def login_user(self, user: User, request: Request) -> TokenResponse:
        access_token, refresh_token, refresh_expires = self._generate_tokens(
            user.id)

        session = UserSession(
            user_id=user.id,
            refresh_token_hash=get_token_hash(refresh_token),
            ip_address=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("User-Agent", "unknown"),
            is_active=True,
            created_at=datetime.utcnow(),
            expires_at=refresh_expires
        )

        self.session.add(session)
        self.session.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    def refresh_token(self, refresh_token: str) -> TokenResponse:
        user_id = self._get_user_id_from_token(refresh_token)

        session = self._get_active_session(user_id, refresh_token)

        new_access_token, new_refresh_token, new_expiry = self._generate_tokens(
            user_id)

        session.refresh_token_hash = get_token_hash(new_refresh_token)
        session.expires_at = new_expiry
        self.session.add(session)
        self.session.commit()

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )

    def logout_user(self, refresh_token: str, current_user: User) -> dict:
        user_id = self._get_user_id_from_token(refresh_token)

        if user_id != current_user.id:
            raise HTTPException(
                403, detail="User not authorized to logout this session.")

        session = self._get_active_session(user_id, refresh_token)

        session.is_active = False
        self.session.add(session)
        self.session.commit()

        return {"message": "Successfully logged out."}

    # ---------- Helpers ----------
    def _get_user_id_from_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = int(payload.get("sub"))
            return user_id
        except (JWTError, TypeError, ValueError):
            raise HTTPException(401, detail="Invalid refresh token.")

    def _get_active_session(self, user_id: int, refresh_token: str) -> UserSession:
        token_hash = get_token_hash(refresh_token)

        session = self.session.exec(
            select(UserSession).where(
                UserSession.user_id == user_id,
                UserSession.refresh_token_hash == token_hash,
                UserSession.is_active == True
            )
        ).first()

        if not session:
            raise HTTPException(401, detail="No active session found.")

        return session
