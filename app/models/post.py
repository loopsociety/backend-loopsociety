from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class PostBase(SQLModel):
    thread_id: int
    content: str

class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    is_first_post: bool = False
    edited_at: Optional[datetime] = None
    edited_by: Optional[int] = None
    upvote_count: int = 0
    downvote_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    user_id: int
    is_first_post: bool
    created_at: datetime
    updated_at: datetime
