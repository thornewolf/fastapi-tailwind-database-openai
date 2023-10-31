from functools import cache, lru_cache
import asyncio

from fastapi import APIRouter, Form, Request, status, BackgroundTasks
from fastapi.responses import (FileResponse, HTMLResponse, RedirectResponse, JSONResponse,
                               Response)

import project.common as common
from project.routers.movie import get_movie
from project.common import templates
from project.llm import llm
from project.routers import blog
from project.routers.reddit_bot import respond_to_posts_forever, get_my_past_10_comments_then_delete_negative_scored

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


@router.get('/search')
async def search(request: Request, description: str = None, raw=False):
    movie_name = get_movie(description)
    if raw:
        return JSONResponse(movie_name)
    print(movie_name)
    amazon_link = f'https://www.amazon.com/s?k={movie_name + " movie"}&ref=nb_sb_noss_2'
    return templates.TemplateResponse("search.jinja", {"request": request, "description": description, "response": movie_name, "movie_link": amazon_link})


@router.on_event("startup")
async def startup():
    asyncio.create_task(respond_to_posts_forever())
    asyncio.create_task(get_my_past_10_comments_then_delete_negative_scored())