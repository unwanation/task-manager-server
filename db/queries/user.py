from uuid import uuid4

from sqlmodel import Session, select

from db import engine
from db.schemas import User


def create(name, email, password):
    uuid = str(uuid4())
    with Session(engine) as session:
        session.add(User(uuid=uuid, name=name, email=email, password=password))
        session.commit()
    return uuid


def remove(user_id):
    with Session(engine) as session:
        user = get_user_by_id(user_id)
        for space in user.spaces:
            for task in space.tasks:
                session.delete(task)
            session.delete(space)
        session.delete(user)
        session.commit()


def alter(user_id, name=None, email=None, password=None):
    with Session(engine) as session:
        user = get_user_by_id(user_id)
        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            user.password = password
        session.commit()


def is_not_exist(user):
    with Session(engine) as session:
        return (
            len(session.exec(select(User).where(User.email == user.email)).all()) == 0
        )


def get_user_by_id(user_id):
    with Session(engine) as session:
        return session.exec(select(User).where(User.uuid == user_id)).first()


def get_user_by_email(email):
    with Session(engine) as session:
        return session.exec(select(User).where(User.email == email)).first()


def get_spaces(user_id):
    with Session(engine) as session:
        return session.exec(select(User).where(User.uuid == user_id)).first().spaces
