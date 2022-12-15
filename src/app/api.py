import os
from dotenv import load_dotenv, find_dotenv
from http import HTTPStatus

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from apischema.encoder import encode_to_json_response, encode_error_to_json_response
from apischema.validator import validate_todo_entry
from entities import TodoEntry
from persistence.mapper.memory import MemoryTodoEntryMapper
from persistence.repository import TodoEntryRepository
from persistence.db import DB

from usecases import get_todo_entry, create_todo_entry, set_todo_label, UseCaseError, NotFoundError

load_dotenv(find_dotenv())
db_connection = DB(host=os.environ.get('DB_HOST'),
                   user=os.environ.get('DB_USER'),
                   pwd=os.environ.get('DB_PWD'),
                   db=os.environ.get('DB_NAME'))


async def get_todo(request: Request) -> Response:
    """
    summary: Finds TodoEntry by id
    parameters:
        - name: id
          in: path
          description: TodoEntry id
          required: true
          schema:
            type: integer
            format: int64
    responses:
        "200":
            description: Object was found.
            examples:
                {"id": 1, "summary": "Lorem Ipsum", "detail": null, "created_at": "2022-09-27T17:29:06.183775+00:00"}
        "404":
            description: Object was not found
    """
    try:
        identifier = request.path_params["id"]  # TODO: add validation

        mapper = MemoryTodoEntryMapper(storage=db_connection)
        repository = TodoEntryRepository(mapper=mapper)

        entity = await get_todo_entry(identifier=identifier, repository=repository)
        content = encode_to_json_response(entity=entity)

    except NotFoundError:
        return Response(
            content=None,
            status_code=HTTPStatus.NOT_FOUND,
            media_type="application/json",
        )

    return Response(content=content, media_type="application/json")


async def create_new_todo_entry(request: Request) -> Response:
    """
    summary: Creates new TodoEntry
    responses:
        "201":
            description: TodoEntry was created.
            examples:
                {"summary": "Lorem Ipsum", "detail": null, "created_at": "2022-09-05T18:07:19.280040+00:00"}
        "422":
            description: Validation error.
        "500":
            description: Something went wrong, try again later.
    """
    data = await request.json()
    errors = validate_todo_entry(raw_data=data)
    if errors:
        return Response(
            content=encode_error_to_json_response(error=errors),
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            media_type="application/json",
        )

    mapper = MemoryTodoEntryMapper(storage=db_connection)
    repository = TodoEntryRepository(mapper=mapper)

    try:
        entity = TodoEntry(**data)
        entity = await create_todo_entry(entity=entity, repository=repository)
        content = encode_to_json_response(entity=entity)
    except UseCaseError:
        return Response(
            content=None,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            media_type="application/json",
        )

    return Response(
        content=content, status_code=HTTPStatus.CREATED, media_type="application/json"
    )


async def set_new_todo_label(request: Request) -> Response:
    try:
        identifier = request.path_params["id"]
        label = request.path_params["label"]

        mapper = MemoryTodoEntryMapper(storage=db_connection)
        repository = TodoEntryRepository(mapper=mapper)

        entity = await set_todo_label(identifier=identifier, label=label, repository=repository)
        content = encode_to_json_response(entity=entity)

    except NotFoundError:
        return Response(
            content=None,
            status_code=HTTPStatus.NOT_FOUND,
            media_type="application/json",
        )
    return Response(
        content=content, status_code=HTTPStatus.CREATED, media_type="application/json"
    )


app = Starlette(
    debug=True,
    routes=[
        Route("/todo/", create_new_todo_entry, methods=["POST"]),
        Route("/todo/{id:int}/", get_todo, methods=["GET"]),
        Route("/todo/{label:str}/{id:int}", set_new_todo_label, methods=["PUT"])
    ],
)
