from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.category import Category, CategoryCreate
from app.core.dependencies import get_current_user
from app.db.database import get_session

router = APIRouter()

@router.post("/", response_model=Category)
def create_category(
    category: CategoryCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    new_category = Category(**category.dict())
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category

@router.get("/", response_model=list[Category])
def get_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()

@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, session: Session = Depends(get_session)):
    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category