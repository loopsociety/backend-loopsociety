from typing import List
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from sqlmodel import Session, select
from fastapi import HTTPException, status
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, thread_id: int) -> UserRead:
        user = self.session.exec(
            select(User).where(User.id == thread_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user = self.session.exec(select(User).where(
            User.id == int(user_id))).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    def get_profile(self, user_id: int) -> UserRead:
        user = self.get_by_id(user_id)
        return UserRead(id=user.id, username=user.username, email=user.email)

    def update_user(self, user_id: int, data: UserUpdate) -> UserRead:
        user = self.get_by_id(user_id)

        if data.username:
            existing = self.get_user_by_username(data.username)
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
            user.username = data.username

        if data.email:
            existing = self.get_user_by_email(data.email)
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
            user.email = data.email

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return UserRead(id=user.id, username=user.username, email=user.email)

    def change_password(self, user_id: int, current_password: str, new_password: str):
        user = self.get_by_id(user_id)

        if not self.verify_password(current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        user.password_hash = self.hash_password(new_password)
        self.session.add(user)
        self.session.commit()
        return {"message": "Password updated successfully"}

    def delete_user(self, user_id: int):
        user = self.get_by_id(user_id)
        self.session.delete(user)
        self.session.commit()
        return {"message": "User deleted"}

    def list_users(self, skip: int = 0, limit: int = 10) -> List[UserRead]:
        users = self.session.exec(select(User).offset(skip).limit(limit)).all()
        return [UserRead(id=u.id, username=u.username, email=u.email) for u in users]
