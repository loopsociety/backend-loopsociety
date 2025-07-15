import pytest
import pytest
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, create_engine


# default session fixture for tests
@pytest.fixture
def session():
    # make a database in memory for testing
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Clean up the database after tests
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def service_factory(session):
    def _create(service_class):
        return service_class(session)
    return _create
