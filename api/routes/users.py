from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.database.connection import get_db
from api.database.schemas.user import UserResponse, UserUpdate, PasswordUpdate
# from api.crud.user import update_password
import api.crud.user as user_crud

from api.token import get_current_user

router = APIRouter()


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.put("/update/{user_id}", response_model=UserResponse)
def update_user_profile(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = user_crud.update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/update-password/{user_id}", summary="Update user password")
def update_password(
    user_id: int,
    data: PasswordUpdate,
    db: Session = Depends(get_db)
):
    user = user_crud.update_password(db, user_id=user_id, new_password=data.new_password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password updated successfully"}

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return user_crud.get_all_users(db)

@router.get("/get/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/delete/{user_id}", summary="Delete user")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
