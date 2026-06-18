from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.department_schema import DepartmentCreate, DepartmentResponse
from app.schemas.employee_schema import EmployeeResponse
from app.controllers.department_controller import (
    create_department_controller, list_departments_controller, get_department_controller
)
from app.dependencies.auth_dependency import require_role, get_current_user
from app.models.user_model import RoleEnum, User

router = APIRouter(prefix="/api/departments", tags=["Departments"])

@router.post("/", response_model=DepartmentResponse, status_code=201)
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    return create_department_controller(db, data)

@router.get("/", response_model=List[DepartmentResponse])
def list_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_departments_controller(db)

@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_department_controller(db, department_id)

@router.get("/{department_id}/employees", response_model=List[EmployeeResponse])
def get_department_employees(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    department = get_department_controller(db, department_id)
    return department.employees