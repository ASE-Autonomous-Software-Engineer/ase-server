from pydantic import BaseModel

class ExecuteTaskRequest(BaseModel):

    objective: str

    repository_path: str