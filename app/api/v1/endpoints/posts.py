from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import get_session
from app.models.user import User
from app.utils.user import get_current_user
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.services.post_service import PostService

router = APIRouter()


@router.get("/", response_model=List[Post])
def list_posts(
    session: Session = Depends(get_session),
):
    return PostService(session).get_all()


@router.get("/{post_id}", response_model=Post)
def get_post(
    post_id: int,
    session: Session = Depends(get_session),
):
    return PostService(session).get_by_id(post_id)


@router.post("/", response_model=Post)
def create_post(
    data: PostCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return PostService(session).create(data, user_id=current_user.id)


@router.put("/{post_id}", response_model=Post)
def update_post(
    post_id: int,
    data: PostUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return PostService(session).update(post_id, data, user_id=current_user.id)


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return PostService(session).delete(post_id, user_id=current_user.id)
