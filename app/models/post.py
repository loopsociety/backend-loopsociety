from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    thread_id: int = Field(foreign_key="threads.id")
    content: str = Field(max_length=2000)
    is_edited: bool = False
    edited_at: Optional[datetime] = None
    edited_by: Optional[int] = None
    upvote_count: int = 0
    downvote_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
