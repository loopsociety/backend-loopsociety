from pydantic import BaseModel
from datetime import datetime


class ThreadCreate(BaseModel):
    title: str
    user_id: int
    category_id: int

class ThreadRead(BaseModel):
    id: int
    title: str
    user_id: int
    category_id: int
    view_count: int
    created_at: datetime
    updated_at: datetime