from datetime import datetime
from logging import lastResort
from typing import List, Optional

from sqlmodel import SQLModel, Field


class BookResponseSchema(SQLModel):
    id: int
    name: str = Field(max_length=32)
    description: str
    link:str
    created_at: datetime
    shelf_id:int
    user_id:int


class BookListResponseSchema(SQLModel):
    items: List[BookResponseSchema]


class BookCreateSchema(SQLModel):
    name: str
    description: Optional[str] = None
    link: Optional[str] = None
    shelf_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)



class BookUpdateSchema(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    shelf_id: Optional[int] = None 