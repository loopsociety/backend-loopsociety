from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import get_session
from app.models.user import User
from app.utils.user import get_current_user
from app.models.thread import Thread
from app.schemas.thread import ThreadCreate, ThreadUpdate
from app.services.thread_service import ThreadService

router = APIRouter()


@router.get("/", response_model=List[Thread])
def list_threads(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    service = ThreadService(session)
    return service.get_paginated(skip=skip, limit=limit)


@router.get("/{thread_id}", response_model=Thread)
def get_thread(
    thread_id: int,
    session: Session = Depends(get_session),
):
    service = ThreadService(session)
    return service.get_by_id(thread_id)


@router.post("/", response_model=Thread)
def create_thread(
    data: ThreadCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ThreadService(session)
    return service.create(data, user_id=current_user.id)


@router.put("/{thread_id}", response_model=Thread)
def update_thread(
    thread_id: int,
    data: ThreadUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ThreadService(session)
    return service.update(thread_id, data, user_id=current_user.id)


@router.delete("/{thread_id}")
def delete_thread(
    thread_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ThreadService(session)
    return service.delete(thread_id, user_id=current_user.id)
