from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task_model import Task, TaskStatusEnum
from app.models.user_model import User, RoleEnum
from app.schemas.task_schema import TaskCreate, TaskStatusUpdate, TaskUpdate, TaskReassign

def create_task(db: Session, data: TaskCreate, created_by_id: int) -> Task:
    employee = db.query(User).filter(User.id == data.assigned_to_id, User.role == RoleEnum.employee).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    new_task = Task(
        title=data.title,
        description=data.description,
        assigned_to_id=data.assigned_to_id,
        created_by_id=created_by_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_all_tasks(db: Session):
    return db.query(Task).all()


def get_task_by_id(db: Session, task_id: int, requesting_user: User) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if requesting_user.role == RoleEnum.employee and task.assigned_to_id != requesting_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only view tasks assigned to you")

    return task


def get_tasks_for_employee(db: Session, employee_id: int):
    return db.query(Task).filter(Task.assigned_to_id == employee_id).all()


def update_task_status(db: Session, task_id: int, employee_id: int, data: TaskStatusUpdate) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if task.assigned_to_id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update tasks assigned to you",
        )

    task.status = data.status
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task_id: int, data: TaskUpdate, requesting_user: User) -> Task:
    task = get_task_by_id(db, task_id, requesting_user)
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, requesting_user: User) -> None:
    task = get_task_by_id(db, task_id, requesting_user)
    db.delete(task)
    db.commit()
    
def reassign_task(db: Session, task_id: int, data: TaskReassign, requesting_user: User) -> Task:
    task = get_task_by_id(db, task_id, requesting_user)

    employee = db.query(User).filter(User.id == data.assigned_to_id, User.role == RoleEnum.employee).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    task.assigned_to_id = data.assigned_to_id
    task.status = TaskStatusEnum.pending  # resets so it doesn't stay "completed" under the new person
    db.commit()
    db.refresh(task)
    return task