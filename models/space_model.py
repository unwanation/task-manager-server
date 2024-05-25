from pydantic import BaseModel


class SpaceModel(BaseModel):
    name: str
    priority: int = 1
    tasks: list = []
