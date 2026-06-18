from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.models.user_model import RoleEnum

class DepartmentBrief(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    department_id: Optional[int] = None

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    department: Optional[DepartmentBrief] = None
    created_at: datetime

    class Config:
        from_attributes = True