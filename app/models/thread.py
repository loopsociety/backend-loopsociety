from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ThreadBase(SQLModel):
    title: str
    slug: str
    category_id: int
    is_pinned: bool = False
    is_locked: bool = False
    is_closed: bool = False

class Thread(SQLModel, table=True):
    __tablename__ = "threads"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    category_id: int = Field(foreign_key="categories.id")
    title: str = Field(max_length=255)
    slug: str = Field(max_length=255)
    view_count: int = Field(default=0)
    is_pinned: bool = False
    is_locked: bool = Field(default=False)
    is_closed: bool = Field(default=False)
    last_post_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ThreadCreate(ThreadBase):
    pass

class ThreadRead(ThreadBase):
    id: int
    title: str
    user_id: int
    category_id: int
    view_count: int
    created_at: datetime
    updated_at: datetime