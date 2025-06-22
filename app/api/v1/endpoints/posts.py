from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.post import Post, PostCreate, PostRead
from app.core.dependencies import get_current_user
from app.db.database import get_session

router = APIRouter()

@router.post("/", response_model=PostRead)
def create_post(
    post: PostCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    new_post = Post(**post.dict(), user_id=current_user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

@router.get("/thread/{thread_id}", response_model=list[PostRead])
def get_posts_by_thread(thread_id: int, session: Session = Depends(get_session)):
    posts = session.exec(select(Post).where(Post.thread_id == thread_id)).all()
    return posts
