from fastapi import APIRouter, status, HTTPException

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from services.shelves.query_builder.shelf import ShelfQueryBuilder
from services.shelves.schemas.shelf import ShelfListResponseSchema, ShelfCreateSchema
from models.shelves import Shelf



shelf_router = APIRouter()

@shelf_router.get("/shelves")
async def get_shelves(session: AsyncSessionDep):
    try:
        shelves = await ShelfQueryBuilder.get_shelves(session)
        return ShelfListResponseSchema(items=shelves)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@shelf_router.get("/shelves/{shelf_id}", response_model=Shelf)
async def get_shelf_by_id(shelf_id:int, session : AsyncSessionDep):
    try:
        shelf = await ShelfQueryBuilder.get_shelf_by_id(session, shelf_id)
        return shelf
    except EmptyQueryResult:
        raise HTTPException(status_code=404, detail="Shelf not found")


@shelf_router.post("/shelf_add", status_code=status.HTTP_201_CREATED)
async def add_shelf(shelf:ShelfCreateSchema, session:AsyncSessionDep):
    try:
        new_shelf = await ShelfQueryBuilder.add_shelf(session, Shelf(**shelf.dict()))
        return new_shelf
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@shelf_router.delete("/shelves/{shelf_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelf(shelf_id:int, session:AsyncSessionDep):
    try:
        await ShelfQueryBuilder.delete_shelf(session, shelf_id)
    except EmptyQueryResult:
        raise HTTPException(status_code=404, detail="Shelf not found")