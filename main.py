from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.db.crud import insert_url_mapping, get_url_mapping, delete_old_entries
from backend.schemas.url import URLRequest, URLResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="frontend")

templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    delete_old_entries(db)
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def create_short_url(request: URLRequest, db: Session = Depends(get_db)):
    try:
        url_mapping = insert_url_mapping(db=db, original_url=request.original_url, short_url=request.short_url)
        return URLResponse(original_url=url_mapping.original_url, short_url=url_mapping.short_url, created_at=url_mapping.created_at)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{short_url}")
async def redirect(short_url, db: Session = Depends(get_db)):
    if (short_url == "favicon.ico"): return
    try:
        url_mapping = get_url_mapping(db=db, short_url=short_url)
        return RedirectResponse(url=url_mapping.original_url)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/{short_url}")
async def redirect(short_url, db: Session = Depends(get_db)):
    try: 
        url_mapping = get_url_mapping(db=db, short_url=short_url)
        print(url_mapping)
        return URLResponse(original_url=url_mapping.original_url, short_url=url_mapping.short_url, created_at=url_mapping.created_at)
    except Exception as e:
        print(e)
        return None 