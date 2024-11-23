import uuid
from datetime import datetime
from app.settings import db


class User(db.Model):
    """
    Represents an authenticating user in the database.

    Attributes:
        id (UUID): Unique identifier for the user (primary key).
        fullname (str, max_length=100): Full names of the user (not nullable).
        email (str, max_length=100): Email address of the user (not nullable).
        password (str, max_length=13, unique=True): Hashed or Encrypted value (not nullable).
        created_at (datetime): Timestamp of user creation (not nullable, defaults to UTC now).
        updated_at (datetime): Timestamp of user update (not nullable, defaults to UTC now, updates on modification).
    """

    __tablename__ = "users"
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.today)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.today,
        onupdate=datetime.today)
