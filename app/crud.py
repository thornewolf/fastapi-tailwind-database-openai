from dataclasses import dataclass
from typing import Annotated

import fastapi
from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from sqlalchemy.orm import Session

import app.common as common
import app.database as database
import app.exceptions as exceptions
import app.models as models
import app.schemas as schemas

models.Base.metadata.create_all(bind=database.engine)


def dep_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def dep_user(request: Request, db=Depends(dep_db)):
    try:
        user_id = common.get_sub_from_jwt(request.session["user"])
    except Exception:
        raise exceptions.UnauthenticatedException(
            "User not found. Please log in again."
        )
    user = get_user(db, user_id)
    if user is None:
        raise exceptions.UnauthenticatedException(
            "User not found. Please log in again."
        )
    return user


def dep_maybe_user(request: Request, db=Depends(dep_db)):
    try:
        user_id = common.get_sub_from_jwt(request.session["user"])
    except Exception:
        return None
    user = get_user(db, user_id)
    return user


def create_user(db, *, user_id: str, email: str = None):
    user = models.User(id=user_id, email=email)
    print(f"Creating user {user_id} with email {email}")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db, user_id: str):
    return db.query(models.User).filter_by(id=user_id).first()
