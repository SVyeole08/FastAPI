from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status

from models import Users
from passlib.context import CryptContext
from database import sessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


dbDependency = Annotated[Session, Depends(get_db)]


class CreateUserReq(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(db: dbDependency, req: CreateUserReq):
    model = Users(
        email=req.email,
        username=req.username,
        first_name=req.first_name,
        last_name=req.last_name,
        hashed_password=bcrypt_context.hash(req.password),
        role=req.role,
        is_active=True
    )

    db.add(model)
    db.commit()
