from random import randint
from datetime import datetime, timezone

from entities import TodoEntry
from persistence.mapper.errors import EntityNotFoundMapperError, CreateMapperError
from persistence.mapper.interfaces import TodoEntryMapperInterface
from persistence.db import DB


class MemoryTodoEntryMapper(TodoEntryMapperInterface):
    _storage: dict

    def __init__(self, storage: DB) -> None:
        self._storage = storage

    async def get(self, identifier: int) -> TodoEntry:
        try:
            return self._get_row(identifier)
        except KeyError:
            raise EntityNotFoundMapperError(f"Entity `id:{identifier}` was not found.")

    async def create(self, entity: TodoEntry) -> TodoEntry:
        try:
            entity.id = self._generate_unique_id()
            self._storage[entity.id] = entity
            return entity
        except TypeError as error:
            raise CreateMapperError(error)

    async def update(self, identifier: int, label: str) -> TodoEntry:
        try:
            entity = self._storage[identifier]
            entity.label = label
            entity.updated_at = datetime.now(tz=timezone.utc)
            return entity
        except TypeError as error:
            raise CreateMapperError(error)

    def _generate_unique_id(self) -> int:
        identifier = randint(1, 10_000)
        while identifier in self._storage:
            identifier = randint(1, 10_000)

        return identifier

    def _get_row(self, identifier):
        query = "SELECT id, summary, detail, label, updated_at, created_at FROM todos WHERE id=%s LIMIT 1"
        self._storage.cursor.execute(query, (identifier,))
        todo_row = self._storage.cursor.fetchone()
        if not todo_row:
            raise KeyError
        return todo_row
