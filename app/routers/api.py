import secrets
from fastapi import APIRouter, Depends, FastAPI, Request, Response
import os

import app.common as common
import libs.utils as utils
import app.crud as crud
import app.exceptions as exceptions
import app.schemas as schemas
import app.auth as auth

logger = utils.logger.getChild(__name__)
if os.getenv("ENV") == "dev":
    router = FastAPI(
        tags=["api"],
    )
else:
    router = FastAPI(
        tags=["api"],
        # TODO: Add this back in when we have a production server
        # servers=[{"url": "https://llm-mmo-production.up.railway.app/api/"}],
        # root_path_in_servers=False,
    )
protected = APIRouter(
    prefix="",
    dependencies=[Depends(auth.dep_api_key)],
)
public = APIRouter(prefix="", tags=["public"])


@public.get("/log-request", summary="Logs that this endpoint was called")
async def log_request():
    """
    Logs that this endpoint was called
    """
    logger.info("log-request called")
    return {"message": "Logged request"}


@protected.post("/notify/", summary="Send a notification to the developer")
async def send_notification(
    message: str,
):
    """
    Notifies the developer of any issues with the service
    """
    common.write_notification(message=message)
    return {"message": "Notification sent in the background"}


router.include_router(protected)
router.include_router(public)
