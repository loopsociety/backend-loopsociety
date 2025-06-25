from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.thread import Thread
from app.schemas.thread import ThreadCreate, ThreadRead
from app.services.auth import get_current_user
from app.db.database import get_session

router = APIRouter()

@router.post("/", response_model=ThreadRead)
def create_thread(
    thread: ThreadCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    new_thread = Thread(**thread.dict(), user_id=current_user.id)
    session.add(new_thread)
    session.commit()
    session.refresh(new_thread)
    return new_thread

@router.get("/", response_model=list[ThreadRead])
def get_threads(session: Session = Depends(get_session)):
    threads = session.exec(select(Thread).order_by(Thread.created_at.desc())).all()
    return threads

@router.get("/{thread_id}", response_model=ThreadRead)
def get_thread(thread_id: int, session: Session = Depends(get_session)):
    thread = session.exec(select(Thread).where(Thread.id == thread_id)).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread
