from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class Status(str, Enum):
    ToDo = "ToDo"
    InProgress = "InProgress"
    Done = "Done"


class Priority(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: str | None = None
    status: Status = Status.ToDo
    priority: Priority = Priority.Medium
    assignee: str | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("title must not be blank or whitespace-only")
        return stripped


class TaskResponse(TaskCreate):
    id: int


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    assignee: str | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError("title must not be blank or whitespace-only")
        return stripped
