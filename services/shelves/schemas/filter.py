from sqlmodel import SQLModel, Field


class ShelfFilter(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)