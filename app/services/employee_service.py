from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User, RoleEnum
from app.models.department_model import Department
from app.schemas.employee_schema import EmployeeCreate
from app.utils.hashing import hash_password

def create_employee(db: Session, data: EmployeeCreate) -> User:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    if data.department_id is not None:
        department = db.query(Department).filter(Department.id == data.department_id).first()
        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    new_employee = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=RoleEnum.employee,
        department_id=data.department_id,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


def get_all_employees(db: Session):
    return db.query(User).filter(User.role == RoleEnum.employee).all()


def get_employee_by_id(db: Session, employee_id: int) -> User:
    employee = db.query(User).filter(User.id == employee_id, User.role == RoleEnum.employee).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee