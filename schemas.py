
from pydantic import BaseModel, Field
from typing import Literal

Priorityliteral = Literal["low", "medium", "high"]
Taskstatusliteral = Literal["pending", "in progress", "completed"]


class CreateTask(BaseModel):
    Title: str = Field(min_length=1, max_length=120)
    Description: str = Field(default="", max_length=2000)
    Priority: Priorityliteral = "medium"
    Taskstatus: Taskstatusliteral = "pending"


class UpdateTask(BaseModel):
    Title: str | None = Field(default=None, min_length=1, max_length=120)
    Description: str | None = Field(default=None, max_length=2000)
    Priority: Priorityliteral | None = None
    Taskstatus: Taskstatusliteral | None = None


class ResponseTask(CreateTask):
    id: int
