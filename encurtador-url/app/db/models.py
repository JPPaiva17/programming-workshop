from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class ShortURL(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_url = Column(Text, nullable=False)
    short_code = Column(String(6), unique=True, nullable=False, index=True)
    hits = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())

