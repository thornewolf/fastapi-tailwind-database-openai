import os

import fastapi
from concurrent.futures import ThreadPoolExecutor
from starlette.middleware.sessions import SessionMiddleware

import project.exceptions as exceptions
from project.common import templates
import project.common as common


async def http_exception_handler(
    request: fastapi.Request, exc: fastapi.exceptions.HTTPException
):
    detail = exc.detail
    print(request, exc, exc.status_code, detail)
    ThreadPoolExecutor().submit(
        lambda: common.write_notification(
            message=f"{request.url.path} {exc} {exc.status_code} {detail}"
        )
    )
    return templates.TemplateResponse(
        "404.jinja",
        {"request": request, "detail": detail},
        status_code=exc.status_code,
    )


def add_middleware(app: fastapi.FastAPI):
    app.add_exception_handler(
        exceptions.UnauthenticatedException,
        lambda r, e: fastapi.responses.RedirectResponse(url=r.url_for("login")),
    )
    app.add_exception_handler(
        exceptions.NotFoundException,
        lambda r, e: templates.TemplateResponse(
            "404.jinja",
            {"request": r, "detail": f"{e} :("},
            status_code=404,
        ),
    )
    app.add_exception_handler(404, http_exception_handler)
    app.add_middleware(SessionMiddleware, secret_key=os.getenv("APP_SECRET_KEY"))
