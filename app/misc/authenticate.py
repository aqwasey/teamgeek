import os
import hashlib
from functools import wraps
from flask import request, jsonify as jr
from app.misc.cache import DataCache
from app.misc.tokens import JWTTokens
from app.misc.messages import INVALID_TOKEN, SERVICE_SUBSCRIBE
from app.settings import logger


class LoginManager:
    """
    ....
    """
    cache = None
    toke = None

    def __init__(self) -> None:
        self.cache = DataCache()
        self.toke = JWTTokens()

    # @staticmethod
    def require_api_key(self, f):
        """
        Request API Key decorator
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            cache_id = None

            if not api_key:
                return jr({'error': SERVICE_SUBSCRIBE}), 401

            try:
                raw_token = self.toke.deserialize(api_key)
                cache_id = self.cache.get_cache(raw_token["email"])
            except Exception as e:
                logger.error(msg=f"[DECODE TOKEN] - Error occured due to {e}")
                return jr({"error":
                           "Invalid token was specified, try again"}), 401

            if not cache_id:
                return jr({'error', INVALID_TOKEN}), 401

            status = self.toke.compare(api_key, cache_id)
            print(status)
            if api_key and status:
                return f(*args, **kwargs)
            return jr({'error': INVALID_TOKEN}), 401
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
