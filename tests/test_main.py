from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.models import Base
from main import app
from backend.db.database import get_db


client = TestClient(app)

DATABASE_URL = "postgresql://test:test@db:5433/test_db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
   try:
       db = TestingSessionLocal()
       yield db
   finally:
       db.close()

app.dependency_overrides[get_db] = override_get_db


def test_create_short_url():
   response = client.post("/", json={"url": "localhost:8000"})
   assert response.status_code == 200
   data = response.json()
   assert "short_url" in data
   short_url = data["short_url"]
   assert short_url is not None and short_url != ""