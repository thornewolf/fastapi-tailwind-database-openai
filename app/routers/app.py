from functools import cache, lru_cache
import asyncio

from fastapi import APIRouter, Form, Request, status, BackgroundTasks
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    RedirectResponse,
    JSONResponse,
    Response,
)

import app.common as common
from app.common import templates
from lib.llm import llm

router = APIRouter(tags=["app"])


async def startup_function():
    ...


@router.on_event("startup")
async def startup():
    asyncio.create_task(startup_function())


@router.get("/", response_class=HTMLResponse, summary="App homepage")
async def index(request: Request):
    """
    App homepage.
    """
    return templates.TemplateResponse("core/index.jinja", {"request": request})
