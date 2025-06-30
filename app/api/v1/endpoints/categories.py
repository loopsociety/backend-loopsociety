from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.db.database import get_session
from app.services.category import create_category, get_category_by_id, get_all_categories, update_category, delete_category

router = APIRouter()


@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, session: Session = Depends(get_session)):
    get_category_by_id(category_id, session)


@router.post("/", response_model=Category)
def create_category(
    category: CategoryCreate,
    session: Session = Depends(get_session),
):
    return create_category(category, session)


@router.get("/", response_model=list[Category])
def get_categories(session: Session = Depends(get_session)):
    return get_all_categories(session)


@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: Session = Depends(get_session)
):
    return update_category(category_id, category, session)


@router.delete("/{category_id}", response_model=Category)
def delete_category(
    category_id: int,
    session: Session = Depends(get_session),
):
    return delete_category(category_id, session)
