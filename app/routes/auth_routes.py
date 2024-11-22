from flask import Blueprint


auth_routes = Blueprint("api_auth", __name__, url_prefix="/api/auth")
