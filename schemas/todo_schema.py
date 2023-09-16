from pydantic import BaseModel

class TodoBase(BaseModel):
    task: str
    status: bool

class TodoCreate(TodoBase):
    pass 

class Todo(TodoBase):
    id: int

    class Config:
        from_attributes = True