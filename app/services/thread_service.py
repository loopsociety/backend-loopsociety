from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.thread import Thread
from app.schemas.thread import ThreadCreate, ThreadUpdate


class ThreadService:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, thread_id: int) -> Thread:
        thread = self.session.exec(
            select(Thread).where(Thread.id == thread_id)).first()
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        return thread

    def get_all(self) -> List[Thread]:
        return self.session.exec(select(Thread)).all()

    def get_paginated(self, skip: int = 0, limit: int = 10) -> List[Thread]:
        return self.session.exec(select(Thread).offset(skip).limit(limit)).all()

    def create(self, data: ThreadCreate, user_id: int) -> Thread:
        new_thread = Thread(**data.model_dump(), user_id=user_id)
        self.session.add(new_thread)
        self.session.commit()
        self.session.refresh(new_thread)
        return new_thread

    def update(self, thread_id: int, data: ThreadUpdate, user_id: int) -> Thread:
        thread = self.get_by_id(thread_id)

        if thread.user_id != user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to update this thread")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(thread, field, value)

        self.session.add(thread)
        self.session.commit()
        self.session.refresh(thread)
        return thread

    def delete(self, thread_id: int, user_id: int) -> None:
        thread = self.get_by_id(thread_id)

        if thread.user_id != user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this thread")

        self.session.delete(thread)
        self.session.commit()
