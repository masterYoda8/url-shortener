from sqlalchemy import Column, Integer, String, DateTime, functions
from sqlalchemy.ext.declarative import declarative_base
from .database import engine
from datetime import datetime, timezone

Base = declarative_base()

class URLMapping(Base):
    __tablename__ = "url_mapping"
    id = Column(Integer, primary_key=True, index=True)
    short_url = Column(String, unique=True, index=True)
    original_url = Column(String)
    created_at = Column(DateTime, server_default=functions.now())

Base.metadata.create_all(bind=engine)
