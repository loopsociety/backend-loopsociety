from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    title: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    reputation: int
    level: str
    email_verified_at: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    is_active: bool
    created_at: datetime
