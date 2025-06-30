from fastapi import Depends, HTTPException
from app.models.category import Category
from sqlmodel import Session, select
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.db.database import get_session


def get_category_by_id(
    category_id: int,
    session: Session = Depends(get_session)
):
    category = session.exec(select(Category).where(
        Category.id == category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def get_all_categories(
    session: Session = Depends(get_session)
):
    return session.exec(select(Category)).all()


def create_category(
    category: CategoryCreate,
    session: Session = Depends(get_session),
):
    new_category = Category(**category.dict())
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category


def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: Session = Depends(get_session)
):
    category = get_category_by_id(category_id, session)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for field, value in category.dict(exclude_unset=True).items():
        setattr(category, field, value)

    session.add(category)
    session.commit()
    session.refresh(category)
    return category

def delete_category(
    category_id: int,
    session: Session = Depends(get_session),
):
    category = get_category_by_id(category_id, session)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    session.delete(category)
    session.commit()
    return category