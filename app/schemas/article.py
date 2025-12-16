# app/schemas/article.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class ArticleCreateSchema(BaseModel):
    title: str
    content: str
    published_date: date  # This must match the attribute used in your code

class ArticleUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published_date: Optional[date] = None
