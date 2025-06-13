from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database.schemas import admin as schemas
from api.crud import admin as crud
from api.database.connection import get_db

router = APIRouter()

@router.get("/get_ll", response_model=list[schemas.AdminResponse])
def read_all_admins(db: Session = Depends(get_db)):
    return crud.get_all_admins(db)

@router.get("/get_by_id/{admin_id}", response_model=schemas.AdminResponse)
def read_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_id(db, admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

@router.post("/post", response_model=schemas.AdminResponse, status_code=status.HTTP_201_CREATED)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud.create_admin(db, admin)

@router.put("/update/{admin_id}", response_model=schemas.AdminResponse)
def update_admin(admin_id: int, admin: schemas.AdminUpdate, db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_id(db, admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return crud.update_admin(db, admin_id, admin)

@router.delete("/delete/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_id(db, admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    crud.delete_admin(db, admin_id)
    return None
