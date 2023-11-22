# Code generated by sqlc. DO NOT EDIT.
# versions:
#   sqlc v1.24.0
# source: query.sql
import dataclasses
import datetime
from typing import AsyncIterator, List, Optional

import sqlalchemy
import sqlalchemy.ext.asyncio

from booktest import models


BOOKS_BY_TAGS = """-- name: books_by_tags \\:many
SELECT 
  book_id,
  title,
  name,
  isbn,
  tags
FROM books
LEFT JOIN authors ON books.author_id = authors.author_id
WHERE tags && :p1\\:\\:varchar[]
"""


@dataclasses.dataclass()
class BooksByTagsRow:
    book_id: int
    title: str
    name: Optional[str]
    isbn: str
    tags: List[str]


BOOKS_BY_TITLE_YEAR = """-- name: books_by_title_year \\:many
SELECT book_id, author_id, isbn, book_type, title, year, available, tags FROM books
WHERE title = :p1 AND year = :p2
"""


CREATE_AUTHOR = """-- name: create_author \\:one
INSERT INTO authors (name) VALUES (:p1)
RETURNING author_id, name
"""


CREATE_BOOK = """-- name: create_book \\:one
INSERT INTO books (
    author_id,
    isbn,
    book_type,
    title,
    year,
    available,
    tags
) VALUES (
    :p1,
    :p2,
    :p3,
    :p4,
    :p5,
    :p6,
    :p7
)
RETURNING book_id, author_id, isbn, book_type, title, year, available, tags
"""


@dataclasses.dataclass()
class CreateBookParams:
    author_id: int
    isbn: str
    book_type: models.BookType
    title: str
    year: int
    available: datetime.datetime
    tags: List[str]


DELETE_BOOK = """-- name: delete_book \\:exec
DELETE FROM books
WHERE book_id = :p1
"""


GET_AUTHOR = """-- name: get_author \\:one
SELECT author_id, name FROM authors
WHERE author_id = :p1
"""


GET_BOOK = """-- name: get_book \\:one
SELECT book_id, author_id, isbn, book_type, title, year, available, tags FROM books
WHERE book_id = :p1
"""


UPDATE_BOOK = """-- name: update_book \\:exec
UPDATE books
SET title = :p1, tags = :p2
WHERE book_id = :p3
"""


UPDATE_BOOK_ISBN = """-- name: update_book_isbn \\:exec
UPDATE books
SET title = :p1, tags = :p2, isbn = :p4
WHERE book_id = :p3
"""


class AsyncQuerier:
    def __init__(self, conn: sqlalchemy.ext.asyncio.AsyncConnection):
        self._conn = conn

    async def books_by_tags(self, *, dollar_1: List[str]) -> AsyncIterator[BooksByTagsRow]:
        result = await self._conn.stream(sqlalchemy.text(BOOKS_BY_TAGS), {"p1": dollar_1})
        async for row in result:
            yield BooksByTagsRow(
                book_id=row[0],
                title=row[1],
                name=row[2],
                isbn=row[3],
                tags=row[4],
            )

    async def books_by_title_year(self, *, title: str, year: int) -> AsyncIterator[models.Book]:
        result = await self._conn.stream(sqlalchemy.text(BOOKS_BY_TITLE_YEAR), {"p1": title, "p2": year})
        async for row in result:
            yield models.Book(
                book_id=row[0],
                author_id=row[1],
                isbn=row[2],
                book_type=row[3],
                title=row[4],
                year=row[5],
                available=row[6],
                tags=row[7],
            )

    async def create_author(self, *, name: str) -> Optional[models.Author]:
        row = (await self._conn.execute(sqlalchemy.text(CREATE_AUTHOR), {"p1": name})).first()
        if row is None:
            return None
        return models.Author(
            author_id=row[0],
            name=row[1],
        )

    async def create_book(self, arg: CreateBookParams) -> Optional[models.Book]:
        row = (await self._conn.execute(sqlalchemy.text(CREATE_BOOK), {
            "p1": arg.author_id,
            "p2": arg.isbn,
            "p3": arg.book_type,
            "p4": arg.title,
            "p5": arg.year,
            "p6": arg.available,
            "p7": arg.tags,
        })).first()
        if row is None:
            return None
        return models.Book(
            book_id=row[0],
            author_id=row[1],
            isbn=row[2],
            book_type=row[3],
            title=row[4],
            year=row[5],
            available=row[6],
            tags=row[7],
        )

    async def delete_book(self, *, book_id: int) -> None:
        await self._conn.execute(sqlalchemy.text(DELETE_BOOK), {"p1": book_id})

    async def get_author(self, *, author_id: int) -> Optional[models.Author]:
        row = (await self._conn.execute(sqlalchemy.text(GET_AUTHOR), {"p1": author_id})).first()
        if row is None:
            return None
        return models.Author(
            author_id=row[0],
            name=row[1],
        )

    async def get_book(self, *, book_id: int) -> Optional[models.Book]:
        row = (await self._conn.execute(sqlalchemy.text(GET_BOOK), {"p1": book_id})).first()
        if row is None:
            return None
        return models.Book(
            book_id=row[0],
            author_id=row[1],
            isbn=row[2],
            book_type=row[3],
            title=row[4],
            year=row[5],
            available=row[6],
            tags=row[7],
        )

    async def update_book(self, *, title: str, tags: List[str], book_id: int) -> None:
        await self._conn.execute(sqlalchemy.text(UPDATE_BOOK), {"p1": title, "p2": tags, "p3": book_id})

    async def update_book_isbn(self, *, title: str, tags: List[str], book_id: int, isbn: str) -> None:
        await self._conn.execute(sqlalchemy.text(UPDATE_BOOK_ISBN), {
            "p1": title,
            "p2": tags,
            "p3": book_id,
            "p4": isbn,
        })
