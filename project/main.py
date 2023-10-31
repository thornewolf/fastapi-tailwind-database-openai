from dotenv import load_dotenv

load_dotenv()

import openai
from absl import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import project.middleware as middleware
import project.routers.app as frontend
from project.routers import api, auth
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
logging.set_verbosity(logging.INFO)

app = FastAPI()
app.mount("/static", StaticFiles(directory="project/static"), name="static")
middleware.add_middleware(app)

app.include_router(auth.router)
app.include_router(api.router)
app.include_router(frontend.router)

sub_app = FastAPI()


@sub_app.get("/", response_class=HTMLResponse, summary="Sub app homepage")
async def index(request: Request):
    return ""


app.mount("/sub", sub_app)


@app.get("/ads.txt")
async def ads_txt(request: Request):
    return HTMLResponse("google.com, pub-5769573634068772, DIRECT, f08c47fec0942fa0")
