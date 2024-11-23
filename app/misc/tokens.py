from typing import Optional
import jwt
from app.settings import app, logger


class JWTTokens:
    """
    A class for handling JWT token creation and validation.

    Attributes:
        algorithm (str): The signing algorithm to use for JWTs.
        key (str): The secret key used to sign and verify JWTs.
    """

    def __init__(self,) -> None:
        self.algorithm = app.config["ALGORITHM"]
        self.key = app.config["JWT_KEY"]

    def serialize(self, data: dict) -> str:
        """
        Encodes the given data into a JWT.

        Args:
            data (dict): The data to be encoded into the JWT.

        Returns:
            str: The encoded JWT as a string, or None if an error occurs.
        """
        try:
            token = jwt.encode(
                payload=data, key=self.key, algorithm=self.algorithm)
            return token.encode("utf-8")
        except jwt.exceptions.PyJWTError as e:
            logger.error(
                msg=f"[SERIALIZE TOKEN] - Error encoding token due to {e}")
            return None

    def deserialize(self, data: dict) -> Optional[dict | str]:
        """
        Decodes and verifies a JWT.

        Args:
            data (str): The encoded JWT.

        Returns:
            dict: The decoded payload, or None if the token is
            invalid or expired.
        """

        try:
            token = jwt.decode(
                data, key=self.key, algorithms=[self.algorithm])
            return token
        except jwt.ExpiredSignatureError:
            return 'Token has expired'
        except jwt.InvalidTokenError:
            return "Invalid token provided"
        except Exception as e:
            logger.error(
                msg=f"[DESERIALIZE TOKEN] - Error could not deserialize due {e}")
            return "Token could not be decoded"

    def compare(self, key1: str, key2: str) -> int:
        """
        Compares the specified claim in two JWTs.

        Args:
            key1 (str): The first JWT.
            key2 (str): The second JWT.
            claim_to_compare (str): The name of the claim to compare.

        Returns:
            bool: True if the claim values are equal, False otherwise.
        """
        try:
            decoded_jwt1 = jwt.decode(
                key1, self.key, algorithms=[self.algorithm])
            decoded_jwt2 = jwt.decode(
                key2, self.key, algorithms=[self.algorithm])
            return decoded_jwt1 == decoded_jwt2
        except jwt.InvalidTokenError as e:
            logger.error(msg=f"[COMPARE TOKEN]\
                          - Error occured whiles comparing value, due to {e}")
            return False
