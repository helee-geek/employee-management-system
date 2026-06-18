from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskStatusUpdate, TaskUpdate, TaskReassign
from app.controllers.task_controller import (
    create_task_controller, list_tasks_controller, get_task_controller,
    my_tasks_controller, update_task_status_controller,
    update_task_controller, reassign_task_controller, delete_task_controller,
)
from app.dependencies.auth_dependency import require_role, get_current_user
from app.models.user_model import RoleEnum, User

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    return create_task_controller(db, data, current_user.id)


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    return list_tasks_controller(db)


@router.get("/my-tasks", response_model=List[TaskResponse])
def my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.employee)),
):
    return my_tasks_controller(db, current_user.id)


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_status(
    task_id: int,
    data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.employee)),
):
    return update_task_status_controller(db, task_id, current_user.id, data)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_task_controller(db, task_id, current_user)

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    return update_task_controller(db, task_id, data, current_user)

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    delete_task_controller(db, task_id, current_user)
    return None

@router.patch("/{task_id}/reassign", response_model=TaskResponse)
def reassign_task(
    task_id: int,
    data: TaskReassign,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin)),
):
    return reassign_task_controller(db, task_id, data, current_user)