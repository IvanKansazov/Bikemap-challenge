from datetime import datetime, timezone

import pytest
from unittest import mock

from entities import TodoEntry
from persistence.mapper.memory import MemoryTodoEntryMapper
from persistence.repository import TodoEntryRepository
from usecases import get_todo_entry, NotFoundError, create_todo_entry, UseCaseError

mock_storage = mock.MagicMock()
mock_cursor = mock.MagicMock()
mock_storage.cursor = mock_cursor


@pytest.mark.asyncio
async def test_get_todo_entry() -> None:
    mapper = MemoryTodoEntryMapper(storage=mock_storage)
    repository = TodoEntryRepository(mapper=mapper)
    mock_storage.cursor.fetchone.return_value = TodoEntry(id=1,
                                                          summary="Lorem Ipsum",
                                                          created_at=datetime.now(tz=timezone.utc))
    entity = await get_todo_entry(identifier=1, repository=repository)
    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_get_not_existing_todo_entry() -> None:
    mapper = MemoryTodoEntryMapper(storage=mock_storage)
    repository = TodoEntryRepository(mapper=mapper)
    mock_storage.cursor.fetchone.return_value = None
    with pytest.raises(NotFoundError):
        await get_todo_entry(identifier=42, repository=repository)


@pytest.mark.asyncio
async def test_create_todo_entry() -> None:
    mapper = MemoryTodoEntryMapper(storage=mock_storage)
    repository = TodoEntryRepository(mapper=mapper)

    data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    mock_storage.cursor.fetchone.return_value = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    entity = await create_todo_entry(entity=data, repository=repository)

    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_todo_entry_creation_error() -> None:
    mapper = MemoryTodoEntryMapper(storage=mock_storage)
    repository = TodoEntryRepository(mapper=mapper)
    mock_storage.cursor.fetchone.return_value = None

    data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    with pytest.raises(UseCaseError):
        await create_todo_entry(entity=data, repository=repository)
