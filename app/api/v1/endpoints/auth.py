from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from app.schemas.user import UserCreate, UserLogin
from app.db.database import get_session
from app.services.auth import authenticate_user, register_user, login_user, refresh_token
from app.schemas.auth import TokenResponse, TokenRefreshRequest

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    return register_user(user.email, user.username, user.password, session)


@router.post("/login")
def login(
    form_data: UserLogin,
    request: Request,
    session: Session = Depends(get_session)
):
    user = authenticate_user(form_data.email, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return login_user(user, request, session)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: TokenRefreshRequest, session: Session = Depends(get_session)):
    return refresh_token(data.refresh_token, session)
