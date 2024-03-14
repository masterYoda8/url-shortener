import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from main import app
from backend.db.models import Base
from backend.db.database import get_db
from fastapi.testclient import TestClient

TEST_DATABASE_URL = "postgresql://user:password@localhost/shortener_test"
engine = create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="session")
def create_test_database():

   # Create test database
   if not database_exists(engine.url):
       create_database(engine.url)

   Base.metadata.create_all(bind=engine)

   yield  # This is where the testing happens

   # Drop test database
   drop_database(engine.url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
app.dependency_overrides[get_db] = db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c