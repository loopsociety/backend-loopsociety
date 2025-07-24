from sqlmodel import Session, create_engine
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
