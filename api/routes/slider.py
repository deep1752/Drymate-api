from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from api.database.schemas.slider import SliderCreate, SliderOut, SliderUpdate
from api.crud import slider as crud_slider
from api.database.connection import get_db

router = APIRouter()

UPLOAD_DIR = "uploads/slider_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/post", response_model=SliderOut)
def create_slider(
    title: str = Form(...),
    subtitle: str = Form(...),
    status: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_path = f"{UPLOAD_DIR}/{image.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    data = SliderCreate(title=title, subtitle=subtitle, status=status)
    return crud_slider.create_slider(db, data, image_path=image_path)

@router.get("/get", response_model=List[SliderOut])
def get_all_sliders(db: Session = Depends(get_db)):
    return crud_slider.get_sliders(db)


@router.get("/get/{slider_id}", response_model=SliderOut)
def get_slider_by_id(slider_id: int, db: Session = Depends(get_db)):
    slider = crud_slider.get_slider(db, slider_id)
    if not slider:
        raise HTTPException(status_code=404, detail="Slider not found")
    return slider


@router.put("/update/{slider_id}", response_model=SliderOut)
def update_slider(
    slider_id: int,
    title: str = Form(...),
    subtitle: str = Form(...),
    status: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if image:
        image_path = f"{UPLOAD_DIR}/{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    data = SliderUpdate(title=title, subtitle=subtitle, status=status)
    updated_slider = crud_slider.update_slider(db, slider_id, data, image_path)
    if not updated_slider:
        raise HTTPException(status_code=404, detail="Slider not found")
    return updated_slider

@router.delete("/delete/{slider_id}")
def delete_slider(slider_id: int, db: Session = Depends(get_db)):
    success = crud_slider.delete_slider(db, slider_id)
    if not success:
        raise HTTPException(status_code=404, detail="Slider not found")
    return {"detail": "Deleted successfully"}
