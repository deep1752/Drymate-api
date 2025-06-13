from sqlalchemy.orm import Session
from api.database.models.user import User
from api.database.schemas.user import UserCreate, UserUpdate
from api.security import hash_password
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


def create_user(db: Session, user: UserCreate):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password),
        mobile=user.mobile,
        age=user.age,
        gender=user.gender,
        role="customer",  # Default role
        created_at=datetime.utcnow(),
        updated_at=None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_mobile(db: Session, mobile: str):
    return db.query(User).filter(User.mobile == mobile).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

# def update_user(db: Session, user_id: int, data: UserUpdate):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         return None
#     for field, value in data.dict(exclude_unset=True).items():
#         setattr(user, field, value)
#     user.updated_at = datetime.utcnow()
#     db.commit()
#     db.refresh(user)
#     return user




def update_user(db: Session, user_id: int, data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    user.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        if "Duplicate entry" in str(e.orig) and "users.mobile" in str(e.orig):
            raise HTTPException(status_code=400, detail="mobile number already exists")
        raise HTTPException(status_code=500, detail="Failed to update user")



def update_password(db: Session, user_id: int, new_password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.password = hash_password(new_password)
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user
