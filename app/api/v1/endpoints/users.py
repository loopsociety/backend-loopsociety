from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.user import User, UserRead
from app.db.database import get_session
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/")
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()
