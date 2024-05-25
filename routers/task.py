from fastapi import APIRouter, Depends, HTTPException
from starlette import status

import db.queries.space
import db.queries.task
import db.queries.user
from db.schemas import User, Task
from deps import get_current_user
from models.task_model import TaskModel

router = APIRouter()


@router.get("/task/get")
async def get_task(task_id, user: User = Depends(get_current_user)) -> Task:
    if not db.queries.task.is_owner(task_id, user.uuid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return db.queries.task.get(task_id)


@router.post("/task/new")
async def create_task(
    task_model: TaskModel, space_id: int, user: User = Depends(get_current_user)
):
    if not db.queries.space.is_owner(space_id, user.uuid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return db.queries.task.create(
        task_model.name,
        task_model.priority,
        task_model.status,
        task_model.deadline,
        space_id,
    )


@router.post("/task/edit")
async def edit_task(
    task_id: int, task_model: TaskModel, user: User = Depends(get_current_user)
):
    if not db.queries.task.is_owner(task_id, user.uuid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    db.queries.task.alter(task_id, **task_model.dict())


@router.post("/task/reassign")
async def reassign_task(
    task_id: int, space_id: int, user: User = Depends(get_current_user)
):
    if not db.queries.task.is_owner(
        task_id, user.uuid
    ) or not db.queries.space.is_owner(space_id, user.uuid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    db.queries.task.reassign(task_id, space_id)
