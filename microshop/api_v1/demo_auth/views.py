import secrets
from time import time
from typing import Annotated, Any
import uuid

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Header,
    HTTPException,
    Response,
    status,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])


security = HTTPBasic()


@router.get("/basic-auth")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "messgae": "Hi!",
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_passwords = {
    "admin": "admin",
    "john": "password",
}


static_auth_token_to_username = {
    "13ca0ba500ff74eee99627e0b14010bb": "admin",
    "b2221367fd23086760e582549c2d4718": "john",
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    # secrets
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc

    return credentials.username


def get_auth_username_by_static_auth_token(
    static_token: Annotated[str, Header(alias="x-auth-token")],
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


@router.get("/basic-auth-username")
def demo_basic_auth_username(
    auth_username: Annotated[str, Depends(get_auth_user_username)]
):
    return {
        "messgae": f"Hi, {auth_username}!",
        "username": auth_username,
    }


@router.get("/some-http-header-auth")
def demo_auth_some_http_header(
    username: Annotated[str, Depends(get_auth_username_by_static_auth_token)]
):
    return {
        "messgae": f"Hi, {username}!",
        "username": username,
    }


COOKIES: dict[str, dict[str, Any]] = {}
# Example
# {
#     "w3g4w3wb3bwsvw4v3v": {"username": "petr", "login_ay": 232352},
#     "wbtsert34gtgs44stw": {"username": "jown", "login_ay": 345345},
# }


COOKIE_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(
    session_id: Annotated[str | None, Cookie(alias=COOKIE_SESSION_ID_KEY)],
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )

    return COOKIES[session_id]


@router.post("/login-cookie")
def demo_auth_login_set_cookie(
    response: Response,
    # auth_username: Annotated[str, Depends(get_auth_user_username)],
    username: Annotated[str, Depends(get_auth_username_by_static_auth_token)],
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": username,
        "login_at": int(time()),
    }
    response.set_cookie(
        COOKIE_SESSION_ID_KEY,
        session_id,
    )
    return {"result": "ok"}


@router.get("/check_cookie")
def demo_auth_check_cookie(
    user_session_data: Annotated[dict, Depends(get_session_data)]
):
    username = user_session_data["username"]
    return {
        "message": f"Hello {username}!",
        **user_session_data,
    }


@router.get("/logout_cookie")
def demo_auth_logout_cookie(
    response: Response,
    session_id: Annotated[str, Cookie(alias=COOKIE_SESSION_ID_KEY)],
    user_session_data: Annotated[dict, Depends(get_session_data)],
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"Bue {username}!",
    }
