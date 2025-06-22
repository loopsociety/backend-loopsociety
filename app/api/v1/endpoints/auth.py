from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models.user import User, UserCreate, UserLogin
from app.db.database import get_session
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(
        User.email == user.email or User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email or Username already registered")

    hashed = hash_password(user.password)
    new_user = User(username=user.username,
                   email=user.email, password_hash=hashed)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"msg": "User created successfully", "user_id": new_user.id}


@router.post("/login")
def login(data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
