import uuid
from datetime import datetime
from typing import List, Optional
from app.models.user import User
from app.settings import db, logger


class UserRepository:
    """
    Provides a layer of abstraction for interacting with User
    data in the database.

    This repository class encapsulates database operations for User objects,
    promoting code reusability and separation of concerns.
    """

    def __init__(self):
        self.db = db

    def create_user(self, item: User) -> User:
        """
        Creates a new user record in the database.

        Args:
            item (User): An instance of the User model with user details.

        Returns:
            Book: The newly created User object with its assigned ID.

        Raises:
            Exception: If an unexpected error occurs during database
            interaction.
        """

        try:
            new_book = User(**item.dict())
            self.db.session.add(new_book)
            self.db.session.commit()
            return new_book
        except Exception as e:
            logger.error(
                "[CREATE USER] - Error creating user due to %s",
                str(e), exc_info=True)
            return None

    def get_user(self, username: str, password: str) -> Optional[User | None]:
        """
        Retrieves a single user record based on its Email and password.

        Args:
            email (str): The email associated with a user account.
            password (str): The unique password associated with a user account

        Returns:
            Optional[Book or None]: The Book object if found, otherwise None.
        """

        data = User.query.filter_by(email=username).one()
        instant_hash = ""
        return data or None

    def update_user(self, item: dict) -> Optional[User | None]:
        """
        Updates an existing book record with new information.

        Args:
            item (dict): A dictionary containing new values for
            specific fields.

        Returns:
            Optional[User]: The updated User object if successful,
            otherwise None.

        Raises:
            Exception: If an unexpected error occurs during database
            interaction.
        """

        try:
            query_id = uuid.UUID(item.id)
            book = User.query.get(query_id)
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
            logger.error("[UPDATE USER] - Invalid UUID format for 'id': %s", e)
            return None
        except Exception as ex:
            logger.error("[UPDATE USER] - Error updating user due to %s",
                         str(ex), exc_info=True)
            return None
