from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.user import UserCreate, UserLogin
from app.db.database import get_session
from app.services.auth import authenticate_user, register_user

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    return register_user(user.email, user.username, user.password, session)


@router.post("/login")
def login(data: UserLogin, session: Session = Depends(get_session)):
    return authenticate_user(data.email, data.password, session)
