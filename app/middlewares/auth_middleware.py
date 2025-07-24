from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from app.db.database import get_session
from app.utils.auth import get_token_hash
from app.models.user import User
from app.models.user_session import UserSession
from sqlmodel import select

EXCLUDED_PREFIX = {
    "/docs", "/openapi", "/redoc",
    "/api/v1/auth/login", "/api/v1/auth/register", "/api/v1/auth/refresh"
}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if self.is_excluded_path(request.url.path):
            return await call_next(request)

        token = self.extract_token(request)
        if not token:
            return self.unauthorized("Authorization header missing or invalid")

        try:
            user_id = self.decode_token(token)
        except JWTError:
            return self.unauthorized("Invalid token")

        session_gen = get_session()
        session = next(session_gen)

        try:
            if not self.is_valid_session(session, user_id, token):
                return self.unauthorized("Session inactive or expired")

            user = self.get_user(session, user_id)
            if not user:
                return JSONResponse(status_code=404, content={"detail": "User not found"})

            request.state.user = user
        finally:
            session_gen.close()

        return await call_next(request)

    def is_excluded_path(self, path: str) -> bool:
        return any(path.startswith(p) for p in EXCLUDED_PREFIX)

    def decode_token(self, token: str) -> int:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))

    def is_valid_session(self, session, user_id: int, token: str) -> bool:
        token_hash = get_token_hash(token)
        statement = select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.refresh_token_hash == token_hash,
            UserSession.is_active == True
        )
        return session.exec(statement).first() is not None

    def extract_token(self, request: Request) -> str | None:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        return auth_header.split(" ")[1]

    def get_user(self, session, user_id: int) -> User | None:
        return session.exec(select(User).where(User.id == user_id)).first()

    def unauthorized(self, message: str) -> JSONResponse:
        return JSONResponse(status_code=401, content={"detail": message})
