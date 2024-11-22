from datetime import date, datetime
from typing import Optional, Union
from pydantic import BaseModel, Field


class BaseItem(BaseModel):
    """
    Base class for representing a book's core information.

    Attributes:
        title (str): Title of the book.
        author (str): Author of the book.
        isbn (str): International Standard Book Number.
        publish_date (date): Date the book was published.
    """

    title: str = Field(min_length=10, max_length=100)
    author: str = Field(min_length=10, max_length=100)
    isbn: str = Field(max_length=13, min_length=10)
    publish_date: date


class CreateItem(BaseItem):
    """
    Model for creating a new book.

    Attributes:
        Inherits all attributes from BaseItem.
        created_at (Optional[datetime]): Optional timestamp of book creation (defaults to now).
    """

    created_at: Optional[datetime] = datetime.now()


class Item(BaseItem):
    """
    Model for representing a book with additional details.

    Attributes:
        Inherits all attributes from BaseItem.
        id (str): Unique identifier for the book.
        created_at (Optional[datetime]): Optional timestamp of book creation (defaults to now).
        updated_at (Optional[datetime]): Optional timestamp of book update (defaults to None).
    """

    id: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = Field(default=None)


class UpdateItem(BaseModel):
    """
    Model for updating an existing book.

    Attributes:
        id (str): Unique identifier for the book.
        title (Union[str, None]): Optional new title for the book.
        author (Union[str, None]): Optional new author for the book.
        isbn (Union[str, None]): Optional new ISBN for the book.
        publish_date (Union[date, None]): Optional new publish date for the book.
    """

    id: str
    title: Union[str, None] = None
    author: Union[str, None] = None
    isbn: Union[str, None] = None
    publish_date: Union[date, None] = None
