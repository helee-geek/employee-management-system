from sqlalchemy.orm import Session
from app.schemas.department_schema import DepartmentCreate
from app.services.department_service import create_department, get_all_departments, get_department_by_id

def create_department_controller(db: Session, data: DepartmentCreate):
    return create_department(db, data)

def list_departments_controller(db: Session):
    return get_all_departments(db)

def get_department_controller(db: Session, department_id: int):
    return get_department_by_id(db, department_id)
