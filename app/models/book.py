import uuid
from datetime import datetime
from app.settings import db


class Book(db.Model):
    """
    Represents a book in the database.

    Attributes:
        id (UUID): Unique identifier for the book (primary key).
        title (str, max_length=100): Title of the book (not nullable).
        author (str, max_length=100): Author of the book (not nullable).
        isbn (str, max_length=13, unique=True): International Standard Book Number (not nullable).
        publish_date (date): Date the book was published (not nullable).
        created_at (datetime): Timestamp of book creation (not nullable, defaults to UTC now).
        updated_at (datetime): Timestamp of book update (not nullable, defaults to UTC now, updates on modification).
    """

    __tablename__ = "books"
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.today)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.today,
        onupdate=datetime.today)
