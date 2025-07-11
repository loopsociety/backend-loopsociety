from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, category_id: int) -> Category:
        category = self.session.exec(
            select(Category).where(Category.id == category_id)
        ).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        return category

    def get_all(self) -> list[Category]:
        return self.session.exec(select(Category)).all()

    def get_paginated(self, skip: int = 0, limit: int = 10) -> list[Category]:
        return self.session.exec(select(Category).offset(skip).limit(limit)).all()

    def exists(self, name: str) -> bool:
        return self.session.exec(
            select(Category).where(Category.name == name)
        ).first() is not None

    def create(self, data: CategoryCreate) -> Category:
        if self.exists(data.name):
            raise HTTPException(
                status_code=400, detail="Category already exists")

        new_category = Category(**data.dict())
        self.session.add(new_category)
        self.session.commit()
        self.session.refresh(new_category)
        return new_category

    def update(self, category_id: int, data: CategoryUpdate) -> Category:
        category = self.get_by_id(category_id)

        for field, value in data.dict(exclude_unset=True).items():
            setattr(category, field, value)

        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def delete(self, category_id: int) -> None:
        category = self.get_by_id(category_id)

        self.session.delete(category)
        self.session.commit()
