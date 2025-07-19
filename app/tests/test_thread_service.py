from datetime import datetime
import pytest
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from app.services.thread_service import ThreadService
from app.models.thread import Thread
from app.schemas.thread import ThreadCreate, ThreadUpdate


@pytest.fixture
def thread_service(session):
    return ThreadService(session)


def test_create_thread(thread_service):
    data = ThreadCreate(title="Test Thread", category_id=1,
                        slug="thread-content")
    thread = thread_service.create(data, user_id=1)
    assert thread.id is not None
    assert thread.title == "Test Thread"
    assert thread.slug == "thread-content"
    assert thread.user_id == 1


def test_get_by_id(thread_service):
    data = ThreadCreate(title="GetById Thread", category_id=1,
                        slug="thread-content")
    created = thread_service.create(data, user_id=2)
    found = thread_service.get_by_id(created.id)
    assert found.id == created.id
    assert found.title == "GetById Thread"
    assert found.slug == "thread-content"
    assert found.user_id == 2
    assert found.category_id == 1


def test_get_by_id_not_found_raises(thread_service):
    with pytest.raises(HTTPException) as exc:
        thread_service.get_by_id(999)
    assert exc.value.status_code == 404


def test_get_all(thread_service):
    thread_service.create(ThreadCreate(
        title="GetById Thread", category_id=1,
        slug="thread-content"), user_id=1)
    thread_service.create(ThreadCreate(
        title="Thread2", category_id=1, slug="thread2"), user_id=1)
    threads = thread_service.get_all()
    assert len(threads) == 2


def test_get_paginated(thread_service):
    for i in range(15):
        thread_service.create(ThreadCreate(
            title=f"Thread{i}", category_id=1, slug=f"thread{i}"), user_id=1)
    threads = thread_service.get_paginated(skip=5, limit=5)
    assert len(threads) == 5
    assert threads[0].title == "Thread5"


def test_update_thread(thread_service):
    created = thread_service.create(ThreadCreate(
        title="Old Title", category_id=1, slug="old-title"), user_id=1)
    update_data = ThreadUpdate(
        title="New Title", category_id=1, updated_at=datetime.now())
    updated = thread_service.update(created.id, update_data, user_id=1)
    assert updated.title == "New Title"
    assert updated.category_id == 1


def test_update_thread_unauthorized(thread_service):
    created = thread_service.create(ThreadCreate(
        title="Title", category_id=1, slug="title-thread"), user_id=1)
    update_data = ThreadUpdate(
        title="Hacked Title", category_id=1, updated_at=datetime.now())
    with pytest.raises(HTTPException) as exc:
        thread_service.update(created.id, update_data, user_id=2)
    assert exc.value.status_code == 403


def test_delete_thread(thread_service, session):
    created = thread_service.create(ThreadCreate(
        title="ToDelete", category_id=1, slug="to-delete"), user_id=1)
    thread_service.delete(created.id, user_id=1)
    result = session.exec(select(Thread).where(
        Thread.id == created.id)).first()
    assert result is None


def test_delete_thread_unauthorized(thread_service):
    created = thread_service.create(ThreadCreate(
        title="Title", category_id=1, slug="title-thread"), user_id=1)
    with pytest.raises(HTTPException) as exc:
        thread_service.delete(created.id, user_id=2)
    assert exc.value.status_code == 403
