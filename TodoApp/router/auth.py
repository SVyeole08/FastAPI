from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status

from models import Users
from passlib.context import CryptContext
from database import sessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


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


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: dbDependency):
    if authenticate_user(form_data.username, form_data.password, db):
        return f"{form_data.username} authenticated successfully."
    return 'Authentication failed.'
