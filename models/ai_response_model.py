from pydantic import BaseModel


class AITaskResponseModel(BaseModel):
    name: str
    priority: int
    deadline: int


class AIResponseModel(BaseModel):
    tasks: list[AITaskResponseModel]
