from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, update

from database.database import SessionLocal, engine
from database.models import Base, ShortURL
from shortener import create_short_url

app = FastAPI()

Base.metadata.create_all(bind=engine)

class ShortenRequest(BaseModel):
    url: str

class ShortenResponse(BaseModel):
    short_code: str
    short_url: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/shorten-url", response_model=ShortenResponse)
async def shorten_url(payload: ShortenRequest, db: Session = Depends(get_db)):
    short_url = create_short_url(db, payload.url)
    return ShortenResponse(
        short_code=short_url.short_code,
        short_url=f"http://localhost:8080/{short_url.short_code}",
    )


@app.get("/{short_code}")
async def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url_entity = db.execute(
        select(ShortURL).where(ShortURL.short_code == short_code)
    ).scalar_one_or_none()

    if not url_entity:
        raise HTTPException(status_code=404, detail="Codigo nao encontrado")

    db.execute(
        update(ShortURL)
        .where(ShortURL.id == url_entity.id)
        .values(hits = (ShortURL.hits + 1))
    )
    db.commit()

    return RedirectResponse(url_entity.original_url, status_code = 302)