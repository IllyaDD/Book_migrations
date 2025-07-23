from typing import List
from sqlmodel import select

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from models.books import Book


class BookQueryBuilder:
    @staticmethod
    async def get_books(session: AsyncSessionDep):
        query = select(Book)
        result = await session.execute(query)
        books = result.scalars().all()
        if not books:
            raise EmptyQueryResult
        return books


    @staticmethod
    async def get_book_by_id(session:AsyncSessionDep, book_id:int) -> Book:
        query = select(Book).where(Book.id == book_id)
        result = await session.execute(query)
        book = result.scalar_one_or_none()
        if not book:
            raise EmptyQueryResult
        return book


    @staticmethod
    async def add_book(session:AsyncSessionDep, book:Book):
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    @staticmethod
    async def delete_book(session:AsyncSessionDep, book_id:int):
        book = await BookQueryBuilder.get_book_by_id(session, book_id)
        await session.delete(book)
        await session.commit()

    @staticmethod
    async def get_book_by_name(session: AsyncSessionDep, book_name: str) -> Book:
        query = select(Book).where(Book.name == book_name)
        result = await session.execute(query)
        book = result.scalar_one_or_none()
        if not book:
            raise EmptyQueryResult
        return book