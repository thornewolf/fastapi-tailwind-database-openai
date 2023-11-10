from fastapi import APIRouter, Depends, FastAPI

import app.common as common
import lib.utils as utils
import app.crud as crud
import app.exceptions as exceptions
import app.schemas as schemas
import app.auth as auth

logger = utils.logger.getChild(__name__)
router = FastAPI(tags=["api"])
protected = APIRouter(
    prefix="", dependencies=[Depends(auth.dep_api_key)], tags=["protected"]
)
public = APIRouter(prefix="", tags=["public"])


@protected.post("/notify/", summary="Send a notification to the developer")
async def send_notification(
    message: str,
):
    """
    Notifies the developer of any issues with the service
    """
    common.write_notification(message=message)
    return {"message": "Notification sent in the background"}


@public.get("/log-request", summary="Logs that this endpoint was called")
async def log_request():
    """
    Logs that this endpoint was called
    """
    logger.info("log-request called")
    return {"message": "Logged request"}


router.include_router(protected)
router.include_router(public)
