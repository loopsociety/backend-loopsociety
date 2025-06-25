from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.db.database import get_session
from app.services.auth import hash_password, authenticate_user

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(
        User.email == user.email or User.username == user.username)).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Email or Username already registered")

    hashed = hash_password(user.password)
    new_user = User(username=user.username,
                    email=user.email, password_hash=hashed)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}


@router.post("/login")
def login(data: UserLogin, session: Session = Depends(get_session)):
    return authenticate_user(data.email, data.password, session)
