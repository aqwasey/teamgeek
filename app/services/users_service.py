"""
import all the required libraries
"""

from app.misc.utils import hash_pwd
from app.misc.serializers import serialize_user
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    """
    Provides business logic operations for managing user data.

    This service class interacts with the UserRepository to perform CRUD
    operations on user objects, promoting separation of concerns and
    improved testability.
    """

    def __init__(self) -> None:
        self.repo = UserRepository()

    def get_user(self, username: str, password: str) -> dict:
        """
        Retrieves a single user record by its email and password.

        Args:
            username (str): Existing or previously set username or email
            password (str): Existing or previously set password

        Returns:
            Optional[User]: The User object if found, otherwise None.
        """

        hashed_password = hash_pwd(password)  # hash the plain password
        book = self.repo.get_user(username=username, password=hashed_password)
        return serialize_user(book) or {}

    def create_user(self, user: User) -> dict:
        """
        Creates a new user record in the database.

        Args:
            user (User): An instance of the User model.

        Returns:
            User: The newly created user object.
        """

        result = self.repo.create_user(user)
        return serialize_user(result) or {}

    def edit_user(self, update_info: dict) -> dict:
        """
        Updates an existing user record with new information.

        Args:
            update_info (dict): A dictionary containing new values for
            specific fields.

        Returns:
            Optional[User]: The updated User object if successful,
            otherwise None or empty dictionary.
        """

        result = self.repo.update_user(update_info)
        return serialize_user(result) or {}
