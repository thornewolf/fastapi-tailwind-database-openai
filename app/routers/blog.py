import json

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse

from app.common import templates

router = APIRouter(prefix="/blog", tags=["blog"])


@router.get("/", response_class=HTMLResponse, summary="Blog")
async def blog(request: Request):
    with open("app/data/blog/blog.json") as f:
        posts = json.load(f)
    return templates.TemplateResponse(
        "blog/index.jinja",
        {
            "request": request,
            "posts": posts,
        },
    )


@router.get("/posts/{slug}", response_class=HTMLResponse, summary="Blog")
async def blog_post(request: Request, slug: str):
    return templates.TemplateResponse(
        f"blog/generated/{slug}.jinja",
        {
            "request": request,
        },
    )
