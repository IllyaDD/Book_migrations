from typing import List
from sqlmodel import select

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from models import Shelf
from models import Book
from services.books.query_builder.book import BookQueryBuilder
from sqlalchemy.orm import selectinload

from services.shelves.schemas import ShelfUpdateSchema
from sqlmodel import select
from sqlalchemy import Select
from services.shelves.schemas import ShelfFilter
from common.schemas import PaginationParams

class ShelfQueryBuilder:
    @staticmethod
    async def get_shelf_pagination(session:AsyncSessionDep, pagination_params:PaginationParams, filters:ShelfFilter) -> Select:
        query_offset, query_limit = pagination_params.page * pagination_params.size, pagination_params.size
        select_query = ShelfQueryBuilder.apply_filters(select(Shelf), filters).offset(query_offset).limit(query_limit)
        result = await session.execute(select_query)
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
    def apply_filters(select_query: Select, filters: ShelfFilter) -> Select:
        if filters and filters.name:
            select_query = select_query.where(Shelf.name.ilike(f'%{filters.name}%'))
        return select_query



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