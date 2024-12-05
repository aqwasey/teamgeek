from flask import Blueprint, jsonify
from pydantic import ValidationError
from app.services.users_service import UserService
from app.misc.params import CreateUser, AuthUser, UserInfo
from app.auth.tokens import JWTTokens
from app.misc.utils import get_params_data
from app.auth.authenticate import LoginManager, PasswordManager
from app.misc.messages import (
    CREATED_USER_FAILED, CREATED_USER_OK,
    NO_USER_PARAM, NO_PARAMS, TOKEN, UPDATE_USER_FAILED,
    USER_NOT_EXIST, RESULTS_KEY, DELETE_USER_FAILED
)


jwt = JWTTokens()
auths = LoginManager()
password_manager = PasswordManager()
user_service = UserService()
user_routes = Blueprint("api_auth", __name__, url_prefix="/api/auth")


@user_routes.route("/in", methods=["POST"])
def get_access():
    """
    Authenticate user
    """
    try:
        params = get_params_data()
        if not params:
            return jsonify({RESULTS_KEY: NO_USER_PARAM}), 400

        info = AuthUser(email=params["userid"], password=params["pwd"])
        data = user_service.get_user(info)

        if not data:
            return jsonify({RESULTS_KEY: USER_NOT_EXIST}), 404

        result = jwt.serialize(data)
        return jsonify({TOKEN: result.decode("utf-8")}), 200

    except ValidationError as er:
        return jsonify({RESULTS_KEY: er.errors(include_url=False)}), 400


@user_routes.route("/", methods=["POST"])
def new_user():
    """
    Create a new user record
    """
    try:
        data, item = get_params_data(), {}
        if not data:
            return jsonify({RESULTS_KEY: NO_PARAMS}), 400

        if data is not None:
            item = CreateUser(
                email=data["email"], fullname=data["fullname"],
                password=password_manager.generate_password_hash(
                    data["password"]))

            data = user_service.create_user(item)
            if not data or data is None:
                return jsonify({RESULTS_KEY: CREATED_USER_FAILED}), 400

            result = jwt.serialize(data)
            return jsonify({RESULTS_KEY: CREATED_USER_OK, TOKEN:
                            result.decode("utf-8")}), 201

    except ValidationError as er:
        return jsonify({RESULTS_KEY: er.errors(include_url=False)}), 400


@user_routes.route("/", methods=["PUT", "PATCH"])
@auths.require_api_key
def edit_user():
    """
    Modify a user record
    """
    try:
        data, item = get_params_data(), {}
        if data is None or data == {}:
            return jsonify({RESULTS_KEY: NO_USER_PARAM}), 400

        item = UserInfo(password=data["pwd"], email=data["userid"], id=id,)
        result = user_service.edit_user(item)
        if result == {}:
            return jsonify({RESULTS_KEY: UPDATE_USER_FAILED}), 400

        return jsonify({RESULTS_KEY: result}), 200

    except ValidationError as er:
        return jsonify({RESULTS_KEY: er.errors(include_url=False)}), 400


@user_routes.route("/", methods=["DELETE"])
@auths.require_api_key
def remove_user():
    """
    Remove a user record
    """
    try:
        data, item = get_params_data(), {}
        if data is None or data == {}:
            return jsonify({RESULTS_KEY: NO_USER_PARAM}), 400

        item = UserInfo(password=data["pwd"], email=data["userid"], id=id,)
        result = user_service.delete_user(item)
        if not result or result == {}:
            return jsonify({RESULTS_KEY: DELETE_USER_FAILED}), 400

        return jsonify({RESULTS_KEY: result}), 200

    except ValidationError as er:
        return jsonify({RESULTS_KEY: er.errors(include_url=False)}), 400
