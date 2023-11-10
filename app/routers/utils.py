import time

import jinja2
from sqlalchemy.orm import Session

import app.crud as crud
import app.exceptions as exceptions
import lib.llm as llm
import app.models as models
import app.schemas as schemas


def render_template(template: str, **kwargs):
    return jinja2.Environment().from_string(source=template).render(**kwargs)


def execute_function(
    db: Session, user: models.User, function_id: str, arguments: dict[str, str]
):
    """
    Execute a function
    """

    function = crud.get_function(db, function_id)
    start = time.time()
    if function is None:
        raise exceptions.NotFoundException("Function not found")

    rendered = render_template(function.template, **arguments)
    llm_response = llm.llm(rendered)
    stop = time.time()
    crud.create_execution(
        db,
        user,
        schemas.FunctionExecutionCreate(
            function_id=function_id,
            start_time=start,
            completion_time=stop,
            status="success",
            input=arguments,
            output=llm_response,
        ),
    )

    if function.execution_count is None:
        function.execution_count = 1
    else:
        function.execution_count += 1
    db.commit()

    return llm_response
