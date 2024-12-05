from app.misc.params import Item
from app.models.book import Book


def serialize_book(book_instance):
    """
    Serialize an sqlalchemy book instance to json using a pydantic model
    """
    if book_instance is None:
        return None

    if isinstance(book_instance, Book):  # Single Book instance
        book_json = Item(
            id=str(book_instance.id),
            isbn=book_instance.isbn,
            title=book_instance.title,
            author=book_instance.author,
            publish_date=book_instance.publish_date,
            created_at=book_instance.created_at,
            updated_at=book_instance.updated_at
        )
        return book_json.model_dump(mode='json')
    else:  # List of Book instances
        serialized_books = [
            Item(
                id=str(book.id),
                isbn=book.isbn,
                title=book.title,
                author=book.author,
                publish_date=book.publish_date,
                created_at=book.created_at,
                updated_at=book.updated_at
            ).model_dump(mode='json') for book in book_instance
        ]
        return serialized_books
