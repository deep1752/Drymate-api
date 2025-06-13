# routes/trainer.py
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from api.database.connection import get_db
from api.crud import trainer as trainer_crud
from api.database.schemas.trainer import TrainerUpdate, TrainerResponse
from api.database.models.trainer import Trainer

router = APIRouter()
UPLOAD_DIR = "uploads/trainers"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_image_url(filename: str) -> str:
    return f"/uploads/trainers/{filename}" if filename else None

@router.post("/", response_model=TrainerResponse)
async def create_trainer(
    name: str = Form(...),
    designation: str = Form(...),
    mobile_number: str = Form(...),
    twitter_link: Optional[str] = Form(""),
    fb_link: Optional[str] = Form(""),
    linkedin_link: Optional[str] = Form(""),
    image: UploadFile = File(...),
    session: Session = Depends(get_db)
):
    try:
        image_filename = f"{datetime.utcnow().timestamp()}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())

        new_trainer = Trainer(
            name=name,
            designation=designation,
            mobile_number=mobile_number,
            twitter_link=twitter_link,
            fb_link=fb_link,
            linkedin_link=linkedin_link,
            image=image_filename
        )
        session.add(new_trainer)
        session.commit()
        session.refresh(new_trainer)

        return TrainerResponse(
            id=new_trainer.id,
            name=new_trainer.name,
            designation=new_trainer.designation,
            mobile_number=new_trainer.mobile_number,
            twitter_link=new_trainer.twitter_link,
            fb_link=new_trainer.fb_link,
            linkedin_link=new_trainer.linkedin_link,
            image=get_image_url(new_trainer.image),
            created_at=new_trainer.created_at,
            updated_at=new_trainer.updated_at
        )

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_all", response_model=List[TrainerResponse])
def read_trainers(db: Session = Depends(get_db)):
    trainers = trainer_crud.get_all_trainers(db)
    return [
        TrainerResponse(
            **{**trainer.__dict__, "image": get_image_url(trainer.image)}
        )
        for trainer in trainers
    ]


@router.get("/get_by_id/{trainer_id}", response_model=TrainerResponse)
def read_trainer(trainer_id: int, db: Session = Depends(get_db)):
    trainer = trainer_crud.get_trainer_by_id(db, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return TrainerResponse(**{**trainer.__dict__, "image": get_image_url(trainer.image)})

@router.put("/update/{trainer_id}", response_model=TrainerResponse)
async def update_trainer(
    trainer_id: int,
    name: str = Form(...),
    designation: str = Form(...),
    mobile_number: str = Form(...),
    twitter_link: Optional[str] = Form(""),
    fb_link: Optional[str] = Form(""),
    linkedin_link: Optional[str] = Form(""),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    trainer = trainer_crud.get_trainer_by_id(db, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    image_filename = trainer.image
    if image:
        image_filename = f"{datetime.utcnow().timestamp()}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())

    trainer_data = TrainerUpdate(
        name=name,
        designation=designation,
        mobile_number=mobile_number,
        twitter_link=twitter_link,
        fb_link=fb_link,
        linkedin_link=linkedin_link,
        image=image_filename
    )

    updated_trainer = trainer_crud.update_trainer(db, trainer_id, trainer_data)
    return TrainerResponse(**{**trainer.__dict__, "image": get_image_url(trainer.image)})

@router.delete("/delete/{trainer_id}")
def delete_trainer(trainer_id: int, db: Session = Depends(get_db)):
    success = trainer_crud.delete_trainer(db, trainer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return {"message": "Trainer deleted successfully"}
