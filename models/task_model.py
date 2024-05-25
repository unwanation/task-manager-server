from pydantic import BaseModel


class TaskModel(BaseModel):
    name: str
    priority: int = 1
    status: bool = False
    deadline: int
