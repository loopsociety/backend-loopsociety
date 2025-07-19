import pytest
from fastapi import HTTPException
import pytest
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine, select

from app.services.category_service import CategoryService
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


@pytest.fixture
def category_service(service_factory):
    return service_factory(CategoryService)


def test_create_category(category_service):
    data = CategoryCreate(name="Test Category", slug="test-category")
    category = category_service.create(data)
    assert category.id is not None
    assert category.name == "Test Category"
    assert category.slug == "test-category"


def test_create_duplicate_category_raises(category_service):
    data = CategoryCreate(name="Duplicate Category", slug="duplicate-category")
    category_service.create(data)
    with pytest.raises(HTTPException) as exc:
        category_service.create(data)
    assert exc.value.status_code == 400


def test_get_by_id(category_service):
    data = CategoryCreate(name="GetById Category", slug="getbyid-category")
    created = category_service.create(data)
    found = category_service.get_by_id(created.id)
    assert found.id == created.id
    assert found.name == "GetById Category"
    assert found.slug == "getbyid-category"


def test_get_by_id_not_found_raises(category_service):
    with pytest.raises(HTTPException) as exc:
        category_service.get_by_id(999)
    assert exc.value.status_code == 404


def test_get_all(category_service):
    category_service.create(CategoryCreate(name="Cat1", slug="cat1"))
    category_service.create(CategoryCreate(name="Cat2", slug="cat2"))
    categories = category_service.get_all()
    assert len(categories) == 2


def test_get_paginated(category_service):
    for i in range(15):
        category_service.create(CategoryCreate(name=f"Cat{i}", slug=f"cat{i}"))
    categories = category_service.get_paginated(skip=5, limit=5)
    assert len(categories) == 5
    assert categories[0].name == "Cat5"


def test_update_category(category_service):
    created = category_service.create(
        CategoryCreate(name="Old Name", slug="old-name"))
    update_data = CategoryUpdate(name="New Name")
    updated = category_service.update(created.id, update_data)
    assert updated.name == "New Name"


def test_delete_category(category_service, session):
    created = category_service.create(
        CategoryCreate(name="ToDelete", slug="to-delete"))
    category_service.delete(created.id)
    result = session.exec(select(Category).where(
        Category.id == created.id)).first()
    assert result is None
