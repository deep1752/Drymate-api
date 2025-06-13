# schemas/trainer.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TrainerBase(BaseModel):
    name: str
    designation: str
    mobile_number: str
    twitter_link: Optional[str] = None
    fb_link: Optional[str] = None
    linkedin_link: Optional[str] = None

class TrainerCreate(TrainerBase):
    image: str  # store filename or relative path

class TrainerUpdate(TrainerBase):
    image: Optional[str] = None

class TrainerResponse(TrainerBase):
    id: int
    image: Optional[str]  # image URL path
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
