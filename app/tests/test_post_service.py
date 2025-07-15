import pytest
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine, select

from app.services.post_service import PostService
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


@pytest.fixture
def post_service(session):
    return PostService(session)


def test_create_post(post_service):
    data = PostCreate(thread_id=1, content="Test Content")
    post = post_service.create(data, user_id=1)
    assert post.id is not None
    assert post.thread_id == 1
    assert post.content == "Test Content"
    assert post.user_id == 1


def test_get_by_id(post_service):
    data = PostCreate(thread_id=1, content="Some Content")
    created = post_service.create(data, user_id=2)
    found = post_service.get_by_id(created.id)
    assert found.id == created.id
    assert found.thread_id == 1
    assert found.content == "Some Content"


def test_get_by_id_not_found_raises(post_service):
    with pytest.raises(HTTPException) as exc:
        post_service.get_by_id(999)
    assert exc.value.status_code == 404


def test_get_all(post_service):
    post_service.create(PostCreate(
        thread_id=1, content="Content1"), user_id=1)
    post_service.create(PostCreate(
        thread_id=2, content="Content2"), user_id=1)
    posts = post_service.get_all()
    assert len(posts) == 2


def test_get_paginated(post_service):
    for i in range(15):
        post_service.create(PostCreate(
            thread_id=1, content=f"Content{i}"), user_id=1)
    posts = post_service.get_paginated(skip=5, limit=5)
    assert len(posts) == 5
    assert posts[0].thread_id == 1


def test_update_post(post_service):
    created = post_service.create(PostCreate(
        thread_id=1, content="Old Content"), user_id=1)
    update_data = PostUpdate(content="Updated Content")
    updated = post_service.update(created.id, update_data, user_id=1)
    assert updated.thread_id == 1
    assert updated.content == "Updated Content"


def test_update_post_unauthorized(post_service):
    created = post_service.create(PostCreate(
        thread_id=1, content="Content"), user_id=1)
    update_data = PostUpdate(content="Hacked Title")
    with pytest.raises(HTTPException) as exc:
        post_service.update(created.id, update_data, user_id=2)
    assert exc.value.status_code == 403


def test_delete_post(post_service, session):
    created = post_service.create(PostCreate(
        thread_id=1, content="DeleteMe"), user_id=1)
    post_service.delete(created.id, user_id=1)
    result = session.exec(select(Post).where(Post.id == created.id)).first()
    assert result is None


def test_delete_post_unauthorized(post_service):
    created = post_service.create(PostCreate(
        thread_id=1, content="Content"), user_id=1)
    with pytest.raises(HTTPException) as exc:
        post_service.delete(created.id, user_id=2)
    assert exc.value.status_code == 403
