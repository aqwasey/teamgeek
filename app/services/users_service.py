"""
import all the required libraries
"""

from app.auth.login_manager import PasswordManager
from app.serializers.user_serializer import serialize_user
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.misc.params import AuthUser
from app.misc.cache import DataCache
from app.auth.tokens import JWTTokens


class UserService:
    """
    Provides business logic operations for managing user data.

    This service class interacts with the UserRepository to perform CRUD
    operations on user objects, promoting separation of concerns and
    improved testability.
    """

    def __init__(self) -> None:
        self.repo = UserRepository()
        self.password_manager = PasswordManager()
        self.cache = DataCache()
        self.token = JWTTokens()

    def get_user(self, info: AuthUser) -> dict:
        """
        Retrieves a single user record by the email and password.

        Args:
            info (AuthUser): Existing or previously set authenticating info
            (username or email)

        Returns:
            Optional[User]: The User object if found, otherwise None.
        """

        hashed_pwd = self.password_manager.generate_password_hash(
            info.password)
        user = self.repo.get_user(username=info.email, password=hashed_pwd)

        if user:
            result = serialize_user(user)
            # cache the final result or found data
            self.cache.set_cache(
                cache_id=user.email, cache_value=self.token.serialize(result))
            return result
        return {}

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

    def delete_user(self, update_info: dict) -> dict:
        """
        Delete an existing user record.

        Args:
            update_info (dict): A dictionary containing new values for
            specific fields.

        Returns:
            Optional[User]: The updated User object if successful,
            otherwise None or empty dictionary.
        """

        result = self.repo.remove_user(update_info)
        return serialize_user(result) or {}
