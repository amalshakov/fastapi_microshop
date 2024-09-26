from microshop.auth import utils as auth_utils
from microshop.users.schemas import UserSchema


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
        # "logged_in_at"
    }
    return auth_utils.encode_jwt(jwt_payload)
