from fastapi import APIRouter, status, HTTPException, Query
from pydantic import ValidationError

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from services.shelves.query_builder.shelf import ShelfQueryBuilder
from services.shelves.schemas import ShelfUpdateSchema
from services.shelves.schemas.shelf import ShelfListResponseSchema, ShelfCreateSchema
from models.shelves import Shelf
from services.shelves.errors import ShelfNotFound


shelf_router = APIRouter()

@shelf_router.get("/shelves", response_model=ShelfListResponseSchema)
async def get_shelves(
    session: AsyncSessionDep,
    shelf_id: int = Query(None, description="Filter by shelf ID"),
):
    try:
        if shelf_id is not None:
            shelf = await ShelfQueryBuilder.get_shelf_by_id(session, shelf_id)
            return ShelfListResponseSchema(items=[shelf])
        else:
            shelves = await ShelfQueryBuilder.get_shelves(session)
            return ShelfListResponseSchema(items=shelves)
    except ShelfNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No shelves found matching the criteria"
        )

@shelf_router.post("/shelves", status_code=status.HTTP_201_CREATED)
async def add_shelf(shelf:ShelfCreateSchema, session:AsyncSessionDep):
    try:
        new_shelf = await ShelfQueryBuilder.add_shelf(session, Shelf(**shelf.model_dump()))
        return new_shelf
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@shelf_router.delete("/shelves/{shelf_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelf(shelf_id:int, session:AsyncSessionDep):
    try:
        await ShelfQueryBuilder.delete_shelf(session, shelf_id)
    except ShelfNotFound:
        raise HTTPException(status_code=404, detail="Shelf not found")

@shelf_router.patch("/shelves/{shelf_id}")
async def update_shelf(session:AsyncSessionDep, shelf_id:int, data:ShelfUpdateSchema):
    try:
        return await ShelfQueryBuilder.update_shelf(session, shelf_id, data)
    except ShelfNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shelf not found")