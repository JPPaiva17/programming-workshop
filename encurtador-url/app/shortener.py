import random
import string
from sqlalchemy.exc import IntegrityError
from app.db.models import ShortURL

ALPHABET = string.ascii_letters + string.digits

def generate_six_random_characters(length: int = 6 ) -> str:
    return "".join(random.choices(ALPHABET, k=length))

def create_short_url(db, original_url: str) -> ShortURL:
    for _ in range (5):
        code = generate_six_random_characters()
        entry = ShortURL(original_url=original_url, short_code=code)
        db.add(entry)
        try:
            db.commit()
            db.refresh(entry)
            return entry
        except IntegrityError:
            db.rollback()
    raise RuntimeError("Não foi possível gerar um código único após várias tentativas")