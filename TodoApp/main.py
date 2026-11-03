from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from database import engine, sessionLocal
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


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
