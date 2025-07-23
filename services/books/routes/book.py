from fastapi import APIRouter, status, HTTPException

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from services.books.query_builder.book import BookQueryBuilder
from services.books.schemas.book import BookListResponseSchema, BookCreateSchema
from models.books import Book
books_router = APIRouter()


@books_router.get('/books')
async def get_books(session: AsyncSessionDep) -> BookListResponseSchema:
    try:
        books = await BookQueryBuilder.get_books(session)
        return BookListResponseSchema(items=books)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@books_router.post('/book_add', status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreateSchema, session: AsyncSessionDep) -> Book:
    try:
        new_book = await BookQueryBuilder.add_book(session, Book(**book.dict()))
        return new_book
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@books_router.get("/book/{book_id}", response_model=Book)
async def get_book_by_id(book_id:int, session : AsyncSessionDep):
    try:
        book = await BookQueryBuilder.get_book_by_id(session, book_id)
        return book
    except EmptyQueryResult:
        raise HTTPException(status_code=404, detail="Book not found")


@books_router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int, session:AsyncSessionDep):
    try:
        await BookQueryBuilder.delete_book(session, book_id)
    except EmptyQueryResult:
        raise HTTPException(status_code=404, detail="Book not found")



@books_router.get("/books/{book_name}", response_model=Book)
async def get_book_by_name(book_name:str, session:AsyncSessionDep):
    try:
        await BookQueryBuilder.get_book_by_name(session, book_name)
    except EmptyQueryResult:
        raise HTTPException(status_code=404, detail="Book not found")