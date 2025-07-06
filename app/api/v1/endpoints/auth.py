from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from app.schemas.user import UserCreate, UserLogin
from app.db.database import get_session
from app.services.auth_service import AuthService
from app.schemas.auth import TokenResponse, TokenRefreshRequest, LogoutRequest
from app.models.user import User
from app.utils.user import get_current_user

router = APIRouter()


@router.post("/register")
def register(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    return AuthService(session).register_user(user.email, user.username, user.password)


@router.post("/login")
def login(
    form_data: UserLogin,
    request: Request,
    session: Session = Depends(get_session)
):
    user = AuthService(session).authenticate_user(
        form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return AuthService(session).login_user(user, request)


@router.post("/logout")
async def logout(
    payload: LogoutRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    refresh_token = payload.refresh_token

    if not refresh_token:
        raise HTTPException(
            status_code=400, detail="Refresh token is required")

    return AuthService(session).logout_user(refresh_token, current_user)


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    data: TokenRefreshRequest,
    session: Session = Depends(get_session)
):
    return AuthService(session).refresh_token(data.refresh_token)
