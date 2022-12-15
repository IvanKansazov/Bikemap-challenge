from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AbstractEntity(BaseModel):
    id: Optional[int]


class TodoEntry(AbstractEntity):
    summary: str
    detail: Optional[str]
    label: Optional[str]
    updated_at: Optional[datetime]
    created_at: datetime
