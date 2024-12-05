from flask import request


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
