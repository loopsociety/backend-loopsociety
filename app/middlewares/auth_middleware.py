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

EXCLUDED_PREFIX = [
    "/docs", "/openapi", "/redoc",
    "/api/v1/auth/login", "/api/v1/auth/register",
    "/api/v1/auth/refresh"
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(p) for p in EXCLUDED_PREFIX):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing or invalid"})

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = int(payload.get("sub"))
        except JWTError as e:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        session = get_session()
        token_hash = get_token_hash(token)

        user_session = session.exec(
            select(UserSession).where(
                UserSession.user_id == user_id,
                UserSession.refresh_token_hash == token_hash,
                UserSession.is_active == True
            )
        ).first()

        if not user_session:
            return JSONResponse(status_code=401, content={"detail": "Session inactive or expired"})

        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            return JSONResponse(status_code=404, content={"detail": "User not found"})

        request.state.user = user
        return await call_next(request)
