from datetime import datetime
from logging import lastResort
from typing import List, Optional
from sqlmodel import SQLModel, Field
from services.books.schemas.book import BookResponseSchema



class ShelfResponseSchema(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime



class ShelfListResponseSchema(SQLModel):
    items: List[ShelfResponseSchema]


class ShelfCreateSchema(SQLModel):
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)