from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.task_schema import TaskCreate, TaskStatusUpdate, TaskUpdate, TaskReassign
from app.services.task_service import (
    create_task, get_all_tasks, get_task_by_id, get_tasks_for_employee, update_task_status,
    update_task, reassign_task, delete_task,
)

def create_task_controller(db: Session, data: TaskCreate, created_by_id: int):
    return create_task(db, data, created_by_id)

def list_tasks_controller(db: Session):
    return get_all_tasks(db)

def get_task_controller(db: Session, task_id: int, requesting_user: User):
    return get_task_by_id(db, task_id, requesting_user)

def my_tasks_controller(db: Session, employee_id: int):
    return get_tasks_for_employee(db, employee_id)

def update_task_status_controller(db: Session, task_id: int, employee_id: int, data: TaskStatusUpdate):
    return update_task_status(db, task_id, employee_id, data)

def update_task_controller(db: Session, task_id: int, data: TaskUpdate, requesting_user: User):
    return update_task(db, task_id, data, requesting_user)

def delete_task_controller(db: Session, task_id: int, requesting_user: User):
    delete_task(db, task_id, requesting_user)
    
def reassign_task_controller(db: Session, task_id: int, data: TaskReassign, requesting_user: User):
    return reassign_task(db, task_id, data, requesting_user)