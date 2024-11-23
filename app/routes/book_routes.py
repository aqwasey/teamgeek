from flask import Blueprint, jsonify as jr
from pydantic import ValidationError
from app.services.books_service import BookService
from app.misc.params import CreateItem, UpdateItem
from app.misc.utils import get_params_data
from app.misc.authenticate import LoginManager
from app.misc.messages import (
    NO_ID_PARAM, NO_PARAMS,
    READ_EMPTY, UPDATE_FAILED,
    DOES_NOT_EXIST, CREATED_FAILED, RESULTS_KEY
)


auths = LoginManager()
book_service = BookService()
book_routes = Blueprint("api_books", __name__, url_prefix="/api/books")


@book_routes.route("/<string:id>", methods=["GET"])
@auths.require_api_key
def get_book(id: str):
    """
    Get a book record by id
    """
    try:
        if not id:
            return jr({"info": NO_ID_PARAM}), 400

        result = book_service.get_book(book_id=id)
        if not result:
            return jr({RESULTS_KEY: DOES_NOT_EXIST}), 404

        return jr({RESULTS_KEY: result}), 200

    except ValidationError as er:
        return jr({RESULTS_KEY: er.errors(include_url=False)}), 400


@book_routes.route("/", methods=["GET"])
@auths.require_api_key
def all_books():
    """
    Get all the book items
    """
    try:
        result = book_service.get_all_books()
        if not result:
            return jr({RESULTS_KEY: READ_EMPTY}), 404

        return jr({RESULTS_KEY: result}), 200

    except ValidationError as er:
        return jr({RESULTS_KEY: er.errors(include_url=False)}), 400


@book_routes.route("/", methods=["POST"])
@auths.require_api_key
def new_book():
    """
    Create a new book record
    """
    try:
        data, item = get_params_data(), {}
        if not data:
            return jr({RESULTS_KEY: NO_PARAMS}), 400

        if data is not None:
            item = CreateItem(
                author=data["author"], title=data["title"], isbn=data["isbn"],
                publish_date=data["publish_date"])

            result = book_service.create_book(item)
            if not result:
                return jr({RESULTS_KEY: CREATED_FAILED}), 400

            return jr({RESULTS_KEY: result}), 201

    except ValidationError as er:
        return jr({RESULTS_KEY: er.errors(include_url=False)}), 400


@book_routes.route("/<string:id>", methods=["PUT", "PATCH"])
@auths.require_api_key
def edit_book(id: str):
    """
    Modify a book record
    """
    try:
        if not id:
            return jr({RESULTS_KEY: NO_ID_PARAM}), 400

        data, item = get_params_data(), {}
        if data is None or data == {}:
            return jr({RESULTS_KEY: NO_PARAMS}), 400

        item = UpdateItem(
            isbn=data["isbn"], title=data["title"], id=id,
            author=data["author"],
            publish_date=data["publish_date"]
        )

        result = book_service.edit_book(item)
        if result == {}:
            return jr({RESULTS_KEY: UPDATE_FAILED}), 400

        return jr({RESULTS_KEY: result}), 200

    except ValidationError as er:
        return jr({RESULTS_KEY: er.errors(include_url=False)}), 400
