from sqlalchemy.orm import Session
from app.schemas.employee_schema import EmployeeCreate
from app.services.employee_service import create_employee, get_all_employees, get_employee_by_id

def create_employee_controller(db: Session, data: EmployeeCreate):
    return create_employee(db, data)

def list_employees_controller(db: Session):
    return get_all_employees(db)

def get_employee_controller(db: Session, employee_id: int):
    return get_employee_by_id(db, employee_id)