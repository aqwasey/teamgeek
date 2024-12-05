"""
import all the required libraries
"""
import uuid
from typing import List

from app.serializers.serializers import serialize_book
from app.models.book import Book
from app.repositories.book_repository import BookRepository


class BookService:
    """
    Provides business logic operations for managing book data.

    This service class interacts with the BookRepository to perform CRUD
    operations on book objects, promoting separation of concerns and
    improved testability.
    """

    def __init__(self) -> None:
        self.repo = BookRepository()

    def get_book(self, book_id: str) -> dict:
        """
        Retrieves a single book record by its ID.

        Args:
            book_id (str): The unique identifier of the book.

        Returns:
            Optional[Book]: The Book object if found, otherwise None.
        """

        query_id = uuid.UUID(book_id)
        book = self.repo.get_book(query_id)
        return serialize_book(book) or {}

    def get_all_books(self) -> List[dict]:
        """
        Retrieves all book records from the database.

        Returns:
            List[Book]: A list containing all Book objects.
        """

        data = self.repo.get_all_books()
        books = serialize_book(data)
        return books or []

    def create_book(self, book: Book) -> dict:
        """
        Creates a new book record in the database.

        Args:
            book (Book): An instance of the Book model.

        Returns:
            Book: The newly created Book object.
        """

        result = self.repo.create_book(book)
        return serialize_book(result) or {}

    def edit_book(self, update_data: dict) -> dict:
        """
        Updates an existing book record with new information.

        Args:
            update_data (dict): A dictionary containing new values for
            specific fields.

        Returns:
            Optional[Book]: The updated Book object if successful,
            otherwise None or empty dictionary.
        """

        result = self.repo.update_book(update_data)
        return serialize_book(result) or {}
