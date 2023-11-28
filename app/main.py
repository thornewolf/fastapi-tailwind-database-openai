from dotenv import load_dotenv

load_dotenv()
import os
import logging

import openai
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

import app.middleware as middleware
import app.routers.app as frontend
from app import auth
from app.routers import api, blog


match os.getenv("ENV"):
    case "prod" | "dev":
        pass
    case other_env:
        raise ValueError(f'ENV variable must be "prod" or "dev", not "{other_env}"')

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
middleware.add_middleware(app)

app.mount("/api", api.router)
app.include_router(frontend.router)
app.include_router(auth.router)
app.include_router(blog.router)

sub_app = FastAPI()


@sub_app.get("/", response_class=HTMLResponse, summary="Sub app homepage")
async def index(request: Request):
    return ""


app.mount("/sub", sub_app)


@app.get("/ads.txt")
async def ads_txt(request: Request):
    return HTMLResponse("google.com, pub-5769573634068772, DIRECT, f08c47fec0942fa0")


@app.get("/favicon.ico")
def get_favicon():
    cache_duration = 3600  # For example, 1 hour in seconds
    headers = {"Cache-Control": f"public, max-age={cache_duration}"}
    return Response(content=b"", media_type="image/x-icon", headers=headers)
