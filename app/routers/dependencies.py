from typing import Callable, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

import app.crud as crud
import app.exceptions as exceptions

T = TypeVar("T")


def get_item_or_404(
    getter: Callable[[Session, str], T], item_id: str, error_message: str, db
) -> T:
    item = getter(db, item_id)
    if item is None:
        raise exceptions.NotFoundException(error_message)
    return item


def ownership_or_404(item: T, user):
    if item.user_id != user.id:
        raise exceptions.NotFoundException(f"{type(item).__name__} not found")
    return item


# def dep_public_function(function_id: str, db=Depends(crud.dep_db)):
#     return get_item_or_404(crud.get_function, function_id, "Function not found", db)


# def dep_owned_function(
#     function=Depends(dep_public_function), user=Depends(crud.dep_user)
# ):
#     return ownership_or_404(function, user)
