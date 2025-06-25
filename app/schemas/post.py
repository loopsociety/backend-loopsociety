from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str
    thread_id: int


class PostRead(BaseModel):
    id: int
    user_id: int
    thread_id: int
    content: str
    created_at: str  # ISO format string for datetime
    updated_at: str  # ISO format string for datetime


class PostUpdate(BaseModel):
    content: str
    is_edited: bool = False
    edited_by: int = None
