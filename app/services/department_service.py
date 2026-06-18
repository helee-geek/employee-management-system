from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.department_model import Department
from app.schemas.department_schema import DepartmentCreate

def create_department(db: Session, department_data: DepartmentCreate) -> Department:
    existing = db.query(Department).filter(Department.name == department_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department already exists."
        )

    new_department = Department(
        name=department_data.name,
        description=department_data.description
    )
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department

def get_all_departments(db: Session):
    return db.query(Department).all()

def get_department_by_id(db: Session, department_id: int) -> Department:
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found."
        )
    return department