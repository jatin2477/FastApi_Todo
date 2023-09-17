from fastapi import FastAPI, Depends, HTTPException, APIRouter
from models.todo_model import TodoModel
from schemas.todo_schema import Todo, TodoCreate
from config.db import SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()


item = APIRouter()
user = APIRouter()

@user.get('/user/')
def get_user():
    return {"Hello User"}

@item.get('/item/')
def get_item():
    return {"Hello Guys, I am a Item..."}

app.include_router(item, tags=['Items'], prefix='/newitem')
app.include_router(user, tags=['User'], prefix='/newuser')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()            


@app.get('/todos/')
def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()

@app.get('/todos/{todo_id}')
def get_todos(todo_id: int, db: Session = Depends(get_db)):
    return db.query(TodoModel).filter(TodoModel.id == todo_id).first()

@app.post('/todo/')
def add_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    add_todo = TodoModel(**todo.model_dump())
    db.add(add_todo)
    db.commit()
    db.refresh(add_todo)
    return add_todo

@app.put('/edit/{todo_id}')
def update_todo(todo_id: int, updated_tod: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    for key, value in updated_tod.model_dump().items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo  


@app.delete('/delete/{todo_id}')
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")
    db.delete(todo)
    db.commit()
    return todo