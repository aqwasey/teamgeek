from flask import request
import hashlib

def get_params_data():
    """
    Retrieve the pass parameter values.

    First check if there were any json values sent through the request object.

    When no json values could be found, check the form values and
    convert to dictionary.

    If nothing or no parameters were passed return None
    """
    if request.content_type == "application/json":
        return request.get_json()
    else:
        data = request.form.to_dict()
        return data if data else None


def generate_password_hash(param: str) -> str:
    """
    Function to hash raw or plain password value

    Attributes:
        param: plain password value

    Returns:
        Hashed password value or None
    """
    result = hashlib.sha512(param.encode()).hexdigest()
    return result or None


def check_password(hashed_password: str, plain_password: str) -> bool:
    """
    Compare the hashed password and a plain password
    """
    current_hashed_password = generate_password_hash(plain_password)
    return hashed_password == current_hashed_password
