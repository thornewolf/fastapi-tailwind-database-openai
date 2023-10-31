from functools import cache, lru_cache
import asyncio

from fastapi import APIRouter, Form, Request, status, BackgroundTasks
from fastapi.responses import (FileResponse, HTMLResponse, RedirectResponse,
                               Response)

import project.common as common
from project.common import templates
from project.llm import llm
from project.routers import blog
from project.routers.reddit_bot import respond_to_posts_forever

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

@common.time_cache(3)
def get_movie(description: str):
    tries = 0
    response = 'BAD'*20
    while len(response) > 30:
        response = llm(f'''{description}''', system=f'''You are an AI that helps people find the movie they are looking for. They will provide you with a description of the movie and you will provide them with the title of the movie. User descriptions may be vague so always make a best effort guess. It's more important in this context to always return some guess than to tell the user they were vague. Limit all responses to just the movie name. If you provide any more content your response will be rejected.''', examples=[])
        tries += 1
        if tries > 3:
            return "Search failed. Please try again."
    return response


@router.get('/search')
async def search(request: Request, description: str = None):
    movie_name = get_movie(description)
    print(movie_name)
    amazon_link = f'https://www.amazon.com/s?k={movie_name + "movie"}&ref=nb_sb_noss_2'
    return templates.TemplateResponse("search.jinja", {"request": request, "description": description, "response": movie_name, "movie_link": amazon_link})


@router.on_event("startup")
async def startup():
    # asyncio.create_task(lambda: common.write_notification("App started"))
    asyncio.create_task(respond_to_posts_forever())