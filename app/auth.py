from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader
from fastapi.exceptions import HTTPException
from starlette.config import Config
import app.crud as crud
import app.common as common
import app.exceptions as exceptions

config = Config(".env")
oauth = OAuth(config)
auth0 = oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)
assert auth0

api_key_header = APIKeyHeader(name="Authorization")


def dep_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header != env.get("API_KEY"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    return api_key_header


router = APIRouter(prefix="", tags=["authentication"])


@router.get("/login")
async def login(request: Request):
    redirect_uri = str(request.url_for("callback"))
    return await auth0.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def callback(request: Request, db=Depends(crud.dep_db)):
    jwt = await auth0.authorize_access_token(request)
    request.session["user"] = jwt
    if crud.get_user(db, common.get_sub_from_jwt(jwt)) is None:
        crud.create_user(
            db, user_id=common.get_sub_from_jwt(jwt), email=jwt["userinfo"]["email"]
        )
    return RedirectResponse(request.url_for("index"))


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    index_url = str(request.url_for("index"))
    logout_url = (
        "https://"
        + env.get("AUTH0_DOMAIN", "")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": index_url,
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
    return RedirectResponse(url=logout_url)
