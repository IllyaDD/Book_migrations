from fastapi import APIRouter, Query, status, HTTPException, Depends
from fastapi_users import FastAPIUsers
from services.user.modules.manager import get_user_manager, auth_backend
from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from services.books.schemas.book import BookListResponseSchema, BookCreateSchema
from models import Book, User
from pydantic import ValidationError
from services.books.schemas import BookUpdateSchema
from services.books.errors import BookNotFound
from typing import Annotated
from common.schemas import PaginationParams
from services.books.schemas import BookFilter
from services.books.query_builder import BookQueryBuilder
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)
current_active_user = fastapi_users.current_user(active=True)

books_router = APIRouter()


@books_router.get("/books", response_model=BookListResponseSchema)
async def get_books(
        session: AsyncSessionDep,
        pagination_params: Annotated[PaginationParams, Depends()],
        book_id: int = Query(None, description="Filter by book ID"),
        book_name: str = Query(None, description="Filter by book name"),
        name: str = Query(None, description="Filter by book name (partial match)"),
        user_id:int = Query(None, description='Find books by user id')
):
    try:
        if book_id is not None:
            book = await BookQueryBuilder.get_book_by_id(session, book_id)
            return BookListResponseSchema(items=[book])
        if book_name is not None:
            book = await BookQueryBuilder.get_book_by_name(session, book_name)
            return BookListResponseSchema(items=[book])
        if user_id is not None:
            books = await BookQueryBuilder.get_book_by_user_id(session, user_id)
            return  BookListResponseSchema(items=books)

        filters = BookFilter(name=name) if name else None
        books = await BookQueryBuilder.get_books_pagination(
            session,
            pagination_params,
            filters
        )
        return BookListResponseSchema(items=books)

    except EmptyQueryResult:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No books found matching the criteria"
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@books_router.get("/users/books")
async def get_users_shelves(
        session: AsyncSessionDep,
        user: User = Depends(current_active_user)
) -> BookListResponseSchema:
    try:
        books = await BookQueryBuilder.get_books_by_user(session, user.id)
        return BookListResponseSchema(firstName=user.first_name, secondName=user.second_name, items=books)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)






@books_router.post('/books', status_code=status.HTTP_201_CREATED)
async def add_book(
        book: BookCreateSchema,
        session: AsyncSessionDep,
        user: User = Depends(current_active_user)
) -> Book:
    try:
        book_data = book.model_dump()
        book_data['user_id'] = user.id
        new_book = await BookQueryBuilder.add_book(session, Book(**book_data))
        return new_book
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@books_router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id: int,
        session: AsyncSessionDep,
        user: User = Depends(current_active_user)
):
    try:
        await BookQueryBuilder.delete_book(session, book_id)
    except BookNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # Consistent status code usage
            detail="Book not found"
        )


@books_router.patch("/books/{book_id}", response_model=Book)
async def update_book(
        book_id: int,
        data: BookUpdateSchema,
        session: AsyncSessionDep,
        user: User = Depends(current_active_user)
) -> Book:
    try:
        return await BookQueryBuilder.update_book(session, book_id, data)
    except BookNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )