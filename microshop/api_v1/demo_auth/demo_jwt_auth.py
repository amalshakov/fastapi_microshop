from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from microshop.api_v1.demo_auth.helpers import (
    create_access_token,
    create_refresh_token,
)
from microshop.auth import utils as auth_utils
from microshop.users.schemas import UserSchema

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/demo-auth/jwt/login")


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


router = APIRouter(prefix="/jwt", tags=["JWT"])

john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)

sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
)


user_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    if not (user := user_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


def get_current_token_payload(
    # credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )

    return payload


def get_current_auth_user(
    payload: Annotated[dict, Depends(get_current_token_payload)],
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := user_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(
    user: Annotated[UserSchema, Depends(get_current_auth_user)],
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: Annotated[UserSchema, Depends(validate_auth_user)],
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/users/me")
def auth_user_check_self_info(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    user: Annotated[UserSchema, Depends(get_current_active_auth_user)],
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "loged_in_at": iat,
    }
