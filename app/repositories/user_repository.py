from datetime import datetime
from typing import Optional
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
            User: The newly created User object with its assigned ID.

        Raises:
            Exception: If an unexpected error occurs during database
            interaction.
        """

        try:
            exists = User.query.filter_by(
                fullname=item.fullname, email=item.email).first()
            if exists:
                return None

            new_user = User(**item.dict())
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user
        except Exception as e:
            logger.error("[CREATE USER] - Error creating user due to %s",
                         str(e), exc_info=True)
            return None

    def get_user(self, username: str, password: str) -> Optional[User | None]:
        """
        Retrieves a single user record based on its Email and password.

        Args:
            username (str): The email associated with a user account.
            password (str): The unique password associated with a user account

        Returns:
            Optional[User or None]: The User object if found, otherwise None.
        """

        try:
            data = User.query.filter_by(email=username).one()
            instant_hash = password

            # compare if both hash values are the same
            if instant_hash == data.password:
                return data
            return None
        except Exception as e:
            logger.error(msg=f"[GET USER] - Error obtaining user info due to {e}")
            return None

    def update_user(self, item: dict) -> Optional[User | None]:
        """
        Updates an existing user record with new information.

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
            user = User.query.get(item.id)
            if user is None:
                return None

            if user:
                user.fullname = item.fullname
                user.email = item.email
                user.password = item.password
                user.updated_at = datetime.today()
                self.db.session.commit()
            return user

        except Exception as ex:
            logger.error("[UPDATE USER] - Error updating user due to %s",
                         str(ex), exc_info=True)
            return None

    def remove_user(self, item: dict) -> Optional[User | None]:
        """
        Remove or Delete an existing user record.

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
            user = User.query.filer_by(email=item.id).one()
            if user is None:
                return None

            if user.password == item.password:
                self.db.session.delete(user)
                self.db.session.commit()
                return user
            return None

        except Exception as ex:
            logger.error("[DELETE USER] - Error deleting user due to %s",
                         str(ex), exc_info=True)
            return None
