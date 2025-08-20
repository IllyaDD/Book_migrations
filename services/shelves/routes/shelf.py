from fastapi import APIRouter, status, HTTPException, Query, Depends
from pydantic import ValidationError

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from services.shelves.query_builder import ShelfQueryBuilder
from services.shelves.schemas import ShelfUpdateSchema
from services.shelves.schemas.shelf import ShelfListResponseSchema, ShelfCreateSchema
from models.shelves import Shelf
from services.shelves.errors import ShelfNotFound
from models import User
from typing import Annotated
from common.schemas import PaginationParams
from services.shelves.schemas import ShelfFilter
from services.user.modules.manager import auth_backend, get_user_manager
from fastapi_users import FastAPIUsers


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)
current_active_user = fastapi_users.current_user(active=True)



shelf_router = APIRouter()


@shelf_router.get("/shelves", response_model=ShelfListResponseSchema)
async def get_shelves(
        session: AsyncSessionDep,
        pagination_params: Annotated[PaginationParams, Depends()],
        shelf_id: int = Query(None, description="Filter by shelf ID"),
        name: str = Query(None, description="Filter by shelf name (partial match)")
):
    try:
        if shelf_id is not None:
            shelf = await ShelfQueryBuilder.get_shelf_by_id(session, shelf_id)
            return ShelfListResponseSchema(items=[shelf])

        filters = ShelfFilter(name=name) if name else None
        shelves = await ShelfQueryBuilder.get_shelf_pagination(
            session,
            pagination_params,
            filters
        )
        return ShelfListResponseSchema(items=shelves)

    except EmptyQueryResult:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No shelves found matching the criteria"
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@shelf_router.get("/users/shelves")
async def get_users_shelves(
        session: AsyncSessionDep,
        user: User = Depends(current_active_user)
) -> ShelfListResponseSchema:
    try:
        shelves = await ShelfQueryBuilder.get_shelves_by_user(session, user.id)
        return ShelfListResponseSchema(firstName=user.first_name, secondName=user.second_name, items=shelves)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@shelf_router.post("/shelves", status_code=status.HTTP_201_CREATED)
async def add_shelf(
        shelf: ShelfCreateSchema,
        session: AsyncSessionDep,
        user: User = Depends(current_active_user)
):
    try:
        shelf_data = shelf.model_dump()
        shelf_data['user_id'] = user.id
        new_shelf = await ShelfQueryBuilder.add_shelf(session, Shelf(**shelf_data))
        return new_shelf
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@shelf_router.delete("/shelves/{shelf_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelf(
        shelf_id: int,
        session: AsyncSessionDep,
        user: User = Depends(current_active_user)
):
    try:
        await ShelfQueryBuilder.delete_shelf(session, shelf_id)
    except ShelfNotFound:
        raise HTTPException(status_code=404, detail="Shelf not found")


@shelf_router.patch("/shelves/{shelf_id}")
async def update_shelf(
        session: AsyncSessionDep,
        shelf_id: int,
        data: ShelfUpdateSchema,
        user: User = Depends(current_active_user)
):
    try:
        return await ShelfQueryBuilder.update_shelf(session, shelf_id, data)
    except ShelfNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shelf not found")
