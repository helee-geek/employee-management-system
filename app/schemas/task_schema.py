from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.task_model import TaskStatusEnum

class EmployeeBrief(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    assigned_to_id: int

class TaskStatusUpdate(BaseModel):
    status: TaskStatusEnum

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = None

class TaskReassign(BaseModel):
    assigned_to_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatusEnum
    assignee: EmployeeBrief
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True