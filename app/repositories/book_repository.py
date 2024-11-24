import uuid
from datetime import datetime
from typing import List, Optional
from app.models.book import Book
from app.settings import db, logger


class BookRepository:
    """
    Provides a layer of abstraction for interacting with Book
    data in the database.

    This repository class encapsulates database operations for Book objects,
    promoting code reusability and separation of concerns.
    """

    def __init__(self):
        self.db = db

    def create_book(self, item: Book) -> Book:
        """
        Creates a new book record in the database.

        Args:
            item (Book): An instance of the Book model with book details.

        Returns:
            Book: The newly created Book object with its assigned ID.

        Raises:
            Exception: If an unexpected error occurs during database
            interaction.
        """

        try:
            exists = Book.query.filter_by(
                isbn=item.isbn, author=item.author, title=item.title).first()

            if exists:
                return None

            new_book = Book(**item.dict())
            self.db.session.add(new_book)
            self.db.session.commit()
            return new_book
        except Exception as e:
            logger.error("[CREATE BOOK] - Error creating book due to %s",
                         str(e), exc_info=True)
            return None

    def get_book(self, book_id: str) -> Optional[Book | None]:
        """
        Retrieves a single book record based on its ID.

        Args:
            book_id (str): The unique identifier of the book to retrieve.

        Returns:
            Optional[Book or None]: The Book object if found, otherwise None.
        """

        data = Book.query.get(book_id)
        return data or None

    def get_all_books(self) -> List[Book]:
        """
        Retrieves all book records from the database.

        Returns:
            List[Book]: A list containing all Book objects.
        """

        return Book.query.all() or []

    def update_book(self, item: dict) -> Optional[Book | None]:
        """
        Updates an existing book record with new information.

        Args:
            item (dict): A dictionary containing new values for
            specific fields.

        Returns:
            Optional[Book]: The updated Book object if successful,
            otherwise None.

        Raises:
            Exception: If an unexpected error occurs during database
            interaction.
        """

        try:
            query_id = uuid.UUID(item.id)
            book = Book.query.get(query_id)
            if book is None:
                return None

            if book:
                book.title = item.title
                book.author = item.author
                book.isbn = item.isbn
                book.publish_date = item.publish_date
                book.updated_at = datetime.today()
                self.db.session.commit()
            return book
        except ValueError as e:
            logger.error("[UPDATE BOOK] - Invalid UUID format for 'id': %s", e)
            return None
        except Exception as ex:
            logger.error("[UPDATE BOOK] - Error updating book due to %s",
                         str(ex), exc_info=True)
            return None
