from sqlmodel import Session, select

from db import engine
from db.schemas import Task


def get(task_id):
    with Session(engine) as session:
        return session.exec(select(Task).where(Task.id == task_id)).first()


def create(name, priority, status, deadline, space_id):
    with Session(engine) as session:
        session.add(
            Task(
                name=name,
                priority=priority,
                status=status,
                deadline=deadline,
                space_id=space_id,
            )
        )
        session.commit()


def remove(task_id):
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id)).first()
        session.delete(task)
        session.commit()


def alter(task_id, name=None, priority=None, status=None, deadline=None):
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id)).first()
        if name:
            task.name = name
        if priority:
            task.priority = priority
        if status:
            task.status = status
        if deadline:
            task.deadline = deadline
        session.commit()


def reassign(task_id, space_id):
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id)).first()
        task.space_id = space_id
        session.commit()


def is_owner(task_id, user_id):
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id)).first()
        return task.space.user_id == user_id
