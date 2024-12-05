from app.misc.params import UserInfo


def serialize_user(user_instance):
    """
    Serialize an sqlalchemy user instance to json using a pydantic model
    """

    if user_instance is None:
        return None

    serialized_user = UserInfo(
        email=user_instance.email,
        password=user_instance.password,
        created_at=user_instance.created_at
    )
    return serialized_user.model_dump(mode='json')
