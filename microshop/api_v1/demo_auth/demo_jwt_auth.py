from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from microshop.api_v1.demo_auth.crud import user_db
from microshop.api_v1.demo_auth.helpers import (
    create_access_token,
    create_refresh_token,
)
from microshop.api_v1.demo_auth.validation import (
    REFRESH_TOKEN_TYPE,
    UserGetterFromToken,
    get_auth_user_from_token_of_type,
    get_current_active_auth_user,
    get_current_auth_user,
    get_current_auth_user_for_refresh,
    get_current_token_payload,
    validate_auth_user,
)
from microshop.auth import utils as auth_utils
from microshop.users.schemas import UserSchema

http_bearer = HTTPBearer(auto_error=False)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
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


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_refresh_jwt(
    user: Annotated[UserSchema, Depends(get_current_auth_user_for_refresh)],
    # user: Annotated[UserSchema,Depends(get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE))],
    # user: Annotated[UserSchema, Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE))],
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
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
