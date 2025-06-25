from sqlmodel import Session, create_engine
from app.core.config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
