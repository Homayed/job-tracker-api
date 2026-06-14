from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import hash_password
from database import get_db
from models import User, JobApplication
from schemas import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="user not found")

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.hashed_password = hash_password(user.password)

    db.commit()
    db.refresh(existing_user)

    return existing_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    existing_application = db.query(JobApplication).filter(
        JobApplication.user_id == user_id
    ).first()

    if existing_application is not None:
        raise HTTPException(
            status_code=400,
            detail="cannot delete user because this user has job applications"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }