from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import VARCHAR, Column


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(sa_column=Column(VARCHAR(32), nullable=False))
    second_name: str = Field(sa_column=Column(VARCHAR(32), nullable=False))
    email: str = Field(sa_column=Column(VARCHAR(255), unique=True, nullable=False))
    hashed_password: str = Field(sa_column=Column(VARCHAR(255), nullable=False))
    is_active: bool = Field(default=True)
    is_super_user: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    published_books: List["Book"] = Relationship(back_populates="user")
    created_shelves: List["Shelf"] = Relationship(back_populates="user")