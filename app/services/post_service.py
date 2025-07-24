from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, post_id: int) -> Post:
        post = self.session.exec(
            select(Post).where(Post.id == post_id)).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    def get_all(self) -> List[Post]:
        return self.session.exec(select(Post)).all()

    def get_paginated(self, skip: int = 0, limit: int = 10) -> List[Post]:
        return self.session.exec(select(Post).offset(skip).limit(limit)).all()

    def create(self, data: PostCreate, user_id: int) -> Post:
        new_post = Post(**data.model_dump(), user_id=user_id)
        self.session.add(new_post)
        self.session.commit()
        self.session.refresh(new_post)
        return new_post

    def update(self, post_id: int, data: PostUpdate, user_id: int) -> Post:
        post = self.get_by_id(post_id)

        if post.user_id != user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to update this post")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(post, field, value)

        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def delete(self, post_id: int, user_id: int) -> None:
        post = self.get_by_id(post_id)

        if post.user_id != user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this post")

        self.session.delete(post)
        self.session.commit()
