from http.client import HTTPException

from sqlalchemy.exc import SQLAlchemyError

from models import User
from connections import SessionLocal
from pydantic import BaseModel, Field, EmailStr
from fastapi import status, Depends, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


class CreateUserRequest(BaseModel):
    id : int
    username: str = Field(min_length=3, max_length=100)
    firstname: str = Field(min_length=3, max_length=100)
    lastname: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=3, max_length=100)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



@router.get('/get', status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    try:
        users = db.query(User).all()
        return users

    except SQLAlchemyError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {str(ex)}"
        )

@router.post('/create',status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserRequest, db: db_dependency):
    try:
        user_model = User(
            id=user.id,
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email
        )

        print(user_model)
        db.add(user_model)
        db.commit()

        return "Success"
    except SQLAlchemyError as ex:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(ex)}"
        )



@router.put('/update_email', status_code=status.HTTP_204_NO_CONTENT)
async def update_email(db:db_dependency,email: str, id: int ):
    try:
        user_model = db.query(User).filter(User.id == id).first()
        user_model.email = email
        print(user_model)
        db.add(user_model)
        db.commit()

    except HTTPException as ex:
        raise ex


@router.delete('/delete/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: db_dependency):
    try:
        user_model = db.query(User).filter(User.id == user_id).first()

        if user_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        db.delete(user_model)
        db.commit()

    except SQLAlchemyError as ex:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {str(ex)}"
        )


