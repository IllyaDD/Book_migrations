from typing import List
from sqlmodel import select

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from models.shelves import Shelf
from sqlalchemy.orm import selectinload


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
        session.commit()
        session.refresh(shelf)
        return shelf