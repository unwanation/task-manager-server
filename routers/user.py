from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import db.queries.space
import db.queries.user
from db.schemas import User, Space
from deps import get_current_user
from models.register_model import RegisterModel
from models.token_model import TokenModel
from utils import (
    get_hashed_password,
    verify_password,
    create_refresh_token,
    create_access_token,
    decode_refresh_token,
)

router = APIRouter()


@router.post("/user/register")
async def register(register_model: RegisterModel):
    if not db.queries.user.is_not_exist(register_model):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    uuid = db.queries.user.create(
        register_model.name,
        register_model.email,
        get_hashed_password(register_model.password),
    )
    db.queries.space.create(
        register_model.name,
        1,
        uuid,
    )


@router.post("/user/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenModel:
    user = db.queries.user.get_user_by_email(form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return TokenModel(
        access_token=create_access_token(user.uuid),
        refresh_token=create_refresh_token(user.uuid),
    )


@router.get("/user/refresh")
async def refresh(token: str) -> TokenModel:
    token_data = decode_refresh_token(token)
    if token_data["exp"] < datetime.now().timestamp():
        raise HTTPException(status_code=401, detail="Token expired")

    user_uuid = token_data["sub"]
    return TokenModel(
        access_token=create_access_token(user_uuid),
        refresh_token=create_refresh_token(user_uuid),
    )


@router.get("/user/get")
async def get_user(user: User = Depends(get_current_user)):
    return {"uuid": user.uuid, "name": user.name, "email": user.email}


@router.get("/user/spaces")
async def get_spaces(user: User = Depends(get_current_user)) -> list[Space]:
    return db.queries.user.get_spaces(user.uuid)
