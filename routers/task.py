from fastapi import APIRouter, Depends, HTTPException
from starlette import status

import ai
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
def create_task(user_input: str, space_id: int, user: User = Depends(get_current_user)):
    if not db.queries.space.is_owner(space_id, user.uuid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        tasks = ai.ai_parse(user_input)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input for ai parse"
        )

    for task in tasks.tasks:
        db.queries.task.create(
            task.name,
            task.priority,
            False,
            task.deadline,
            space_id,
        )


@router.delete("/task/delete")
async def delete_task(task_id: int, user: User = Depends(get_current_user)):
    if not db.queries.task.is_owner(task_id, user.uuid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    db.queries.task.remove(task_id)


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
