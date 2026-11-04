from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import engine, sessionLocal
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class TodoReq(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool = Field(default=False)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


dbDependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
def read_todos(db: dbDependency):
    return db.query(models.Todo).all()


@app.get("/todos/{id}", status_code=status.HTTP_200_OK)
def read_todo_by_id(db: dbDependency, id: int = Path(gt=0)):
    todo_model = db.query(models.Todo).filter(models.Todo.id == id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Todo of id {id} not found")


@app.post('/todos', status_code=status.HTTP_201_CREATED)
def create_todo(db: dbDependency, todo: TodoReq):
    todo_model = models.Todo(**todo.model_dump())
    db.add(todo_model)
    db.commit()


@app.put("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo_by_id(db: dbDependency, todo: TodoReq, id: int = Path(gt=0)):
    todo_model = db.query(models.Todo).filter(models.Todo.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f'Todo of id {id} not found')
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.completed = todo.completed
    db.commit()


@app.delete('/todos/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_id(db: dbDependency, id: int = Path(gt=0)):
    todo_model = db.query(models.Todo).filter(models.Todo.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f'todo of id {id} not found')
    db.query(models.Todo).filter(models.Todo.id == id).delete()
    db.commit()
