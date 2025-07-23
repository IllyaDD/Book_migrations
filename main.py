from contextlib import asynccontextmanager

from fastapi import FastAPI

from common.settings import Settings
from db.database import Database
from services.books.routes.book import books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(settings=Settings())
    yield
    await database.dispose(close=False)


app = FastAPI(lifespan=lifespan)


app.include_router(books_router, tags=['books'])
