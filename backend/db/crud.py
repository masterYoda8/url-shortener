from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.db.models import URLMapping
from datetime import datetime, timedelta, timezone


def insert_url_mapping(db: Session, original_url: str, short_url: str) -> URLMapping:
    new_url_mapping = URLMapping(original_url=original_url, short_url=short_url)
    db.add(new_url_mapping)
    try:
        db.commit()
        return new_url_mapping
    except IntegrityError:
        db.rollback()
    raise Exception("Failed to insert new URLMapping: " + URLMapping)

def get_url_mapping(db: Session, short_url: str) -> URLMapping:
    url_mapping = db.query(URLMapping).filter(URLMapping.short_url == short_url).first()
    if (url_mapping):
        return url_mapping
    else:
        raise Exception("Did not find corresponding long url for short url: " + short_url)

def delete_old_entries(db: Session) -> None:
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=90)
    db.query(URLMapping).filter(URLMapping.created_at < cutoff_date).delete()
    db.commit()
    return