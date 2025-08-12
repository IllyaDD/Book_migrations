from typing import List
from sqlmodel import select

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from models.books import Book
from services.books.schemas import BookUpdateSchema
from common.schemas import PaginationParams
from services.books.schemas import BookFilter
from services.books.schemas import BookFilter
from sqlalchemy import Select
class BookQueryBuilder:

    @staticmethod
    async def get_books_pagination(session:AsyncSessionDep, pagination_params:PaginationParams, filters:BookFilter) -> Select:
        query_offset, query_limit = pagination_params.page * pagination_params.size, pagination_params.size
        select_query = BookQueryBuilder.apply_filters(select(Book), filters).offset(query_offset).limit(query_limit)
        result = await session.execute(select_query)
        books = result.scalars().all()
        if not books:
            raise EmptyQueryResult
        return books
    
    @staticmethod
    def apply_filters(select_query: Select, filters: BookFilter) -> Select:
        if filters and filters.name:
            select_query = select_query.where(Book.name.ilike(f'%{filters.name}%'))
        return select_query


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

    @staticmethod
    async def update_book(session:AsyncSessionDep, book_id:int, data:BookUpdateSchema):
        book = await BookQueryBuilder.get_book_by_id(session, book_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        await session.commit()
        await session.refresh(book)
        return book