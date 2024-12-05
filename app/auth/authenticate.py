import os
import hashlib
from functools import wraps
from flask import request, jsonify as jr
from app.misc.cache import DataCache
from app.auth.tokens import JWTTokens
from app.misc.messages import INVALID_TOKEN, SERVICE_SUBSCRIBE, ERROR
from app.settings import logger


class LoginManager:
    """
    ....
    """
    cache = None
    token = None

    def __init__(self) -> None:
        self.cache = DataCache()
        self.token = JWTTokens()

    # @staticmethod
    def require_api_key(self, f):
        """
        Request API Key decorator
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')

            if not api_key:
                return jr({ERROR: SERVICE_SUBSCRIBE}), 401

            try:
                cache_id = None
                raw_token = self.token.deserialize(api_key)
                cache = self.cache.get_cache(raw_token["email"])
                cache_id = cache

                if not cache_id:
                    return jr({ERROR, INVALID_TOKEN}), 401

                status = self.token.compare(api_key, cache_id.encode("utf-8"))
                if api_key and status:
                    return f(*args, **kwargs)

                return jr({ERROR: INVALID_TOKEN}), 401
            except Exception as e:
                logger.error(msg=f"[DECODE TOKEN] - Error occured due to {e}")
                return jr({ERROR:
                           "Invalid token was specified, try again"}), 401
        return decorated


class PasswordManager:
    """
    Class for managing the hashing and checking of hashed password value

    """
    def generate_password_hash(self, param: str) -> str:
        """
        Function to hash raw or plain password value

        Attributes:
            param: plain password value

        Returns:
            Hashed password value or None
        """
        result = hashlib.sha512(param.encode()).hexdigest()
        return result or None

    def check_password(self, hashed_pwd: str, plain_pwd: str) -> bool:
        """
        Compare the hashed password and a plain password
        """
        current_hashed_password = self.generate_password_hash(plain_pwd)
        return hashed_pwd == current_hashed_password
