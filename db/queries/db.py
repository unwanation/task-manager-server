from sqlmodel import Session, select

from db import engine
from db.schemas import User, Space, Task


# dangerous!!!
def clear():
    with Session(engine) as session:
        for table in (User, Space, Task):
            for entry in session.exec(select(table)).all():
                session.delete(entry)

        session.commit()
