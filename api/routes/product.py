from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import shutil, os
from api.database.connection import get_db
from api.database.schemas.product import ProductOut, ProductCreate, ProductUpdate
from api.crud import product as crud_product

router = APIRouter()

UPLOAD_DIR = "uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/get_all", response_model=List[ProductOut])
def read_products(db: Session = Depends(get_db)):
    return crud_product.get_all_products(db)

@router.get("/get_by_id{product_id}", response_model=ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/post", response_model=ProductOut)
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    discount: float = Form(0.0),
    final_price: float = Form(...),
    discripction: str = Form(...),
    status: str = Form("active"),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if image:
        file_location = f"{UPLOAD_DIR}/{image.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = file_location

    product_data = ProductCreate(
        name=name,
        price=price,
        discount=discount,
        final_price=final_price,
        discripction=discripction,
        status=status,
    )
    return crud_product.create_product(db, product_data, image_path)

@router.put("/update/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    name: str = Form(...),
    price: float = Form(...),
    discount: float = Form(0.0),
    final_price: float = Form(...),
    discripction: str = Form(...),
    status: str = Form("active"),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if image:
        file_location = f"{UPLOAD_DIR}/{image.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = file_location

    product_data = ProductUpdate(
        name=name,
        price=price,
        discount=discount,
        final_price=final_price,
        discripction=discripction,
        status=status,
    )
    updated = crud_product.update_product(db, product_id, product_data, image_path)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud_product.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}
