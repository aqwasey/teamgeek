from flask import Blueprint, json, jsonify as jr
from pydantic import ValidationError
from app.services.users_service import UserService
from app.misc.params import CreateUser, AuthUser, UserInfo
from app.misc.tokens import JWTTokens
from app.misc.utils import get_params_data
from app.misc.authenticate import PasswordManager
from app.misc.messages import (
    CREATED_USER_FAILED, CREATED_USER_OK,
    NO_USER_PARAM, NO_PARAMS, TOKEN, UPDATE_USER_FAILED,
    USER_NOT_EXIST, RESULTS_KEY
)


tk = JWTTokens()
pm = PasswordManager()
auth_service = UserService()
auth_routes = Blueprint("api_auth", __name__, url_prefix="/api/auth")


@auth_routes.route("/in", methods=["POST"])
def get_access():
    """
    Authenticate user
    """
    try:
        params = get_params_data()
        if not params:
            return jr({RESULTS_KEY: NO_USER_PARAM}), 400

        info = AuthUser(email=params["userid"], password=params["pwd"])
        data = auth_service.get_user(info)

        if not data:
            return jr({RESULTS_KEY: USER_NOT_EXIST}), 404

        result = tk.serialize(data)
        return jr({TOKEN: result.decode("utf-8")}), 200

    except ValidationError as er:
        return jr({RESULTS_KEY: er.errors(include_url=False)}), 400


@auth_routes.route("/", methods=["POST"])
def new_user():
    """
    Create a new user record
    """
    try:
        data, item = get_params_data(), {}
        if not data:
            return jr({RESULTS_KEY: NO_PARAMS}), 400

        if data is not None:
            item = CreateUser(
                email=data["email"], fullname=data["fullname"],
                password=pm.generate_password_hash(data["password"]))

            data = auth_service.create_user(item)
            if not data or data is None:
                return jr({RESULTS_KEY: CREATED_USER_FAILED}), 400

            result = tk.serialize(data)
            return jr({RESULTS_KEY: CREATED_USER_OK,
                       TOKEN: result.decode("utf-8")}), 201

    except ValidationError as er:
        return jr({RESULTS_KEY: er.errors(include_url=False)}), 400


@auth_routes.route("/", methods=["PUT", "PATCH"])
def edit_user():
    """
    Modify a user record
    """
    try:
        data, item = get_params_data(), {}
        if data is None or data == {}:
            return jr({RESULTS_KEY: NO_USER_PARAM}), 400

        item = UserInfo(
            password=data["pwd"],
            email=data["userid"], id=id,
        )

        result = auth_service.edit_user(item)
        if result == {}:
            return jr({RESULTS_KEY: UPDATE_USER_FAILED}), 400

        return jr({RESULTS_KEY: result}), 200

    except ValidationError as er:
        return jr({RESULTS_KEY: er.errors(include_url=False)}), 400


@auth_routes.route("/", methods=["DELETE"])
def remove_user():
    """
    Remove a user record
    """
    try:
        data, item = get_params_data(), {}
        if data is None or data == {}:
            return jr({RESULTS_KEY: NO_USER_PARAM}), 400

        item = UserInfo(
            password=data["pwd"], email=data["userid"], id=id,
        )

        result = auth_service.edit_user(item)
        if not result or result == {}:
            return jr({RESULTS_KEY: UPDATE_USER_FAILED}), 400

        return jr({RESULTS_KEY: result}), 200

    except ValidationError as er:
        return jr({RESULTS_KEY: er.errors(include_url=False)}), 400
