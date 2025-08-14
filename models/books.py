from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, VARCHAR
from sqlmodel import Field, SQLModel, Relationship


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(sa_column=Column(VARCHAR(100), nullable=False))
    description: Optional[str] = Field(sa_column=Column(VARCHAR(500), nullable=True))
    link: Optional[str] = Field(sa_column=Column(VARCHAR(500), nullable=True))
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow))
    shelf_id: int = Field(foreign_key="shelves.id", nullable=False)
    shelf: "Shelf" = Relationship(back_populates="books")
    user_id: int = Field(foreign_key="users.id", nullable=False)
    user: "User" = Relationship(back_populates="published_books")