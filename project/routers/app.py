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

import project.common as common
from project.common import templates
from project.llm import llm
from project.routers import blog

router = APIRouter()
router.include_router(blog.router)


@router.get("/", response_class=HTMLResponse, summary="App homepage")
async def index(request: Request):
    """
    App homepage.
    """
    return templates.TemplateResponse("index.jinja", {"request": request})


@router.get("/favicon.ico")
def get_favicon():
    cache_duration = 3600  # For example, 1 hour in seconds
    headers = {"Cache-Control": f"public, max-age={cache_duration}"}
    return Response(content=b"", media_type="image/x-icon", headers=headers)


@router.get("/demo")
async def demo(request: Request):
    return templates.TemplateResponse("demo.jinja", {"request": request})


async def startup_function():
    ...


@router.on_event("startup")
async def startup():
    asyncio.create_task(startup_function())
