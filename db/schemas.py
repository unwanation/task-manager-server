from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    uuid: str = Field(primary_key=True, unique=True, index=True)
    name: str
    email: str
    password: str

    spaces: list["Space"] = Relationship(back_populates="user")


class Space(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str
    priority: int

    user_id: str = Field(foreign_key="user.uuid")
    user: "User" = Relationship(back_populates="spaces")

    tasks: list["Task"] = Relationship(back_populates="space")


class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str
    priority: int
    status: bool
    deadline: int
    space_id: int = Field(foreign_key="space.id")
    space: "Space" = Relationship(back_populates="tasks")
