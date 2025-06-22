from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class UserSession(SQLModel, table=True):
    __tablename__ = "user_sessions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    refresh_token_hash: str
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
