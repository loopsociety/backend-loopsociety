from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.models.category import Category
from app.db.database import get_session
from app.utils.user import get_current_user
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Category])
def list_categories(
    session: Session = Depends(get_session),
):
    service = CategoryService(session)
    return service.get_all()


@router.post("/", response_model=Category)
def create_category(
    data: CategoryCreate,
    session: Session = Depends(get_session),
):
    return CategoryService(session).create(data)


@router.get("/{category_id}", response_model=Category)
def get_category(
    category_id: int,
    session: Session = Depends(get_session),
):
    return CategoryService(session).get_by_id(category_id)


@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    session: Session = Depends(get_session),
):
    return CategoryService(session).update(category_id, data)


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    session: Session = Depends(get_session),
):
    return CategoryService(session).delete(category_id)
