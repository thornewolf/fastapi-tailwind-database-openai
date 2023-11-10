from fastapi import APIRouter, Depends

import app.common as common
import app.crud as crud
import app.exceptions as exceptions
import app.schemas as schemas

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/notify/", summary="Send a notification to the developer")
async def send_notification(
    message: str,
):
    """
    Notifies the developer of any issues with the service
    """
    common.write_notification(message=message)
    return {"message": "Notification sent in the background"}
