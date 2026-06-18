from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse
from app.controllers.employee_controller import (
    create_employee_controller, list_employees_controller, get_employee_controller
)
from app.dependencies.auth_dependency import require_role
from app.models.user_model import RoleEnum, User

router = APIRouter(prefix="/api/employees", tags=["Employees"])

@router.post("/", response_model=EmployeeResponse, status_code=201)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    return create_employee_controller(db, data)

@router.get("/", response_model=List[EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    return list_employees_controller(db)

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    return get_employee_controller(db, employee_id)