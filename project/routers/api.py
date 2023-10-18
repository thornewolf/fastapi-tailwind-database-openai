from fastapi import APIRouter, Depends

import project.common as common
import project.crud as crud
import project.exceptions as exceptions
import project.schemas as schemas

router = APIRouter(prefix="/api", tags=["api"])
functions = APIRouter(prefix="/functions", tags=["api"])
router.include_router(functions)


@router.post("/notify/", summary="Send a notification to the developer")
async def send_notification(
    message: str,
):
    """
    Notifies the developer of any issues with the service
    """
    common.write_notification(message=message)
    return {"message": "Notification sent in the background"}
