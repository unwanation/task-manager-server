from sqlmodel import Session, select

from db import engine
from db.schemas import Space


def create(name, priority, user_id):
    with Session(engine) as session:
        session.add(Space(name=name, priority=priority, user_id=user_id))
        session.commit()


def remove(space_id):
    with Session(engine) as session:
        space = session.exec(select(Space).where(Space.id == space_id)).first()
        for task in space.tasks:
            session.delete(task)
        session.delete(space)
        session.commit()


def alter(space_id, name=None, priority=None):
    with Session(engine) as session:
        space = session.exec(select(Space).where(Space.id == space_id)).first()
        if name:
            space.name = name
        if priority:
            space.priority = priority
        session.commit()


def is_owner(space_id, user_id):
    with Session(engine) as session:
        space = session.exec(select(Space).where(Space.id == space_id)).first()
        return space.user_id == user_id


def get_tasks(space_id):
    with Session(engine) as session:
        return session.exec(select(Space).where(Space.id == space_id)).first().tasks
