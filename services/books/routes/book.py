from fastapi import APIRouter, Query, status, HTTPException, Depends
from watchfiles import awatch

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from services.books.query_builder.book import BookQueryBuilder
from services.books.schemas.book import BookListResponseSchema, BookCreateSchema
from models.books import Book
from pydantic import ValidationError
from services.books.schemas import BookUpdateSchema
from services.books.errors import BookNotFound
from typing import Annotated
from common.schemas import PaginationParams
from services.books.schemas import BookFilter
books_router = APIRouter()

@books_router.get("/books", response_model=BookListResponseSchema)
async def get_books(
    session: AsyncSessionDep,
    pagination_params: Annotated[PaginationParams, Depends()],
    book_id: int = Query(None, description="Filter by book ID"),
    book_name: str = Query(None, description="Filter by book name"),
    name: str = Query(None, description="Filter by book name (partial match)")
):
    try:
        if book_id is not None:
            book = await BookQueryBuilder.get_book_by_id(session, book_id)
            return BookListResponseSchema(items=[book])
        if book_name is not None:
            book = await BookQueryBuilder.get_book_by_name(session, book_name)
            return BookListResponseSchema(items=[book])
        
        
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
@books_router.post('/books', status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreateSchema, session: AsyncSessionDep) -> Book:
    try:
        new_book = await BookQueryBuilder.add_book(session, Book(**book.model_dump()))
        return new_book
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@books_router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int, session:AsyncSessionDep):
    try:
        await BookQueryBuilder.delete_book(session, book_id)
    except BookNotFound:
        raise HTTPException(status_code=404, detail="Book not found")



@books_router.patch("/books/{book_id}")
async def update_book(session:AsyncSessionDep, book_id:int, data:BookUpdateSchema):
    try:
        return await BookQueryBuilder.update_book(session, book_id, data)
    except BookNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")