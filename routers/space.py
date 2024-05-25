from fastapi import APIRouter, Depends, HTTPException
from starlette import status

import db.queries.space
import db.queries.user
from db.schemas import User, Task
from deps import get_current_user
from models.space_model import SpaceModel

router = APIRouter()


@router.get("/space/tasks")
async def get_tasks(space_id, user: User = Depends(get_current_user)) -> list[Task]:
    if not db.queries.space.is_owner(space_id, user.uuid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return db.queries.space.get_tasks(space_id)


@router.post("/space/new")
async def create_space(space_model: SpaceModel, user: User = Depends(get_current_user)):
    db.queries.space.create(space_model.name, space_model.priority, user.uuid)


@router.post("/space/rename")
async def rename_space(
    space_id: int, name: str, user: User = Depends(get_current_user)
):
    if not db.queries.space.is_owner(space_id, user.uuid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    db.queries.space.alter(space_id, name=name)


@router.post("/space/prioritise")
async def prioritise(
    space_id: int, priority: bool, user: User = Depends(get_current_user)
):
    if not db.queries.space.is_owner(space_id, user.uuid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    db.queries.space.alter(space_id, priority=priority)
