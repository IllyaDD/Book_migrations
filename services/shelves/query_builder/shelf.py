from typing import List
from sqlmodel import select

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from models import Shelf
from models import Book
from services.books.query_builder.book import BookQueryBuilder
from sqlalchemy.orm import selectinload

from services.shelves.schemas import ShelfUpdateSchema


class ShelfQueryBuilder:
    @staticmethod
    async def get_shelves(session: AsyncSessionDep):
        query = select(Shelf)
        result = await session.execute(query)
        shelves = result.scalars().all()
        if not shelves:
            raise EmptyQueryResult
        return shelves

    @staticmethod
    async def get_shelf_by_id(session: AsyncSessionDep, shelf_id: int) -> Shelf:
        query = select(Shelf).where(Shelf.id == shelf_id)
        result = await session.execute(query)
        shelf = result.scalar_one_or_none()
        if not shelf:
            raise EmptyQueryResult
        return shelf

    @staticmethod
    async def add_shelf(session:AsyncSessionDep, shelf:Shelf):
        session.add(shelf)
        await session.commit()
        await session.refresh(shelf)
        return shelf

    @staticmethod
    async def delete_shelf(session:AsyncSessionDep, shelf_id):
        shelf = await ShelfQueryBuilder.get_shelf_by_id(session, shelf_id)
        await session.delete(shelf)
        await session.commit()



    @staticmethod
    async def get_shelf_by_book_id(session:AsyncSessionDep, book_id:int):
        book =  await BookQueryBuilder.get_book_by_id(session, book_id)
        if not book:
            return EmptyQueryResult
        query = select(Shelf).where(Shelf.id == book.shelf_id)
        result = await session.execute(query)
        shelf = result.scalars().first()
        if not shelf:
            return EmptyQueryResult
        return shelf




    @staticmethod
    async def update_shelf(session:AsyncSessionDep, shelf_id:int, data:ShelfUpdateSchema):
        shelf = await ShelfQueryBuilder.get_shelf_by_id(session, shelf_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(shelf, key, value)
            await session.commit()
            await session.refresh(shelf)
        return shelf

