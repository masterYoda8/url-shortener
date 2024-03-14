from pydantic import BaseModel
from datetime import datetime

class URLRequest(BaseModel):
    short_url: str
    original_url: str

class URLResponse(BaseModel):
    short_url: str
    original_url: str
    created_at: datetime 