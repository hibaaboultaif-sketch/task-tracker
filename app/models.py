from enum import Enum
import re

from pydantic import BaseModel, ConfigDict, field_validator


class Status(str, Enum):
    ToDo = "ToDo"
    InProgress = "InProgress"
    Done = "Done"


class Priority(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


def _validate_title(v: str) -> str:
    stripped = v.strip()
    if not stripped:
        raise ValueError("title must not be blank or whitespace-only")
    return stripped


def _validate_tags(v: list[str]) -> list[str]:
    cleaned = []
    for tag in v:
        stripped = tag.strip()
        if stripped:
            cleaned.append(stripped)
    return cleaned


def _validate_due_date(v: str | None) -> str | None:
    if v is None:
        return v
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
        raise ValueError("due_date must be in YYYY-MM-DD format")
    return v


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: str | None = None
    status: Status = Status.ToDo
    priority: Priority = Priority.Medium
    assignee: str | None = None
    due_date: str | None = None
    tags: list[str] = []

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        return _validate_title(v)

    @field_validator("tags")
    @classmethod
    def tags_must_be_clean(cls, v: list[str]) -> list[str]:
        return _validate_tags(v)

    @field_validator("due_date")
    @classmethod
    def due_date_format(cls, v: str | None) -> str | None:
        return _validate_due_date(v)


class TaskResponse(TaskCreate):
    id: int
    is_overdue: bool = False


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    assignee: str | None = None
    due_date: str | None = None
    tags: list[str] | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return _validate_title(v)

    @field_validator("tags")
    @classmethod
    def tags_must_be_clean(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return v
        return _validate_tags(v)

    @field_validator("due_date")
    @classmethod
    def due_date_format(cls, v: str | None) -> str | None:
        return _validate_due_date(v)