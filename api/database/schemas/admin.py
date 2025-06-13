from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AdminBase(BaseModel):
    brand_name: str
    email: EmailStr
    mobile_number: str
    address: Optional[str] = None
    twiter_link: Optional[str] = None
    linkedin_link: Optional[str] = None
    fb_link: Optional[str] = None
    insta_link: Optional[str] = None
    youtube_link: Optional[str] = None
    expirence_in_year: Optional[int] = None
    complet_project_numbers: Optional[int] = None
    happy_clint_numbers: Optional[int] = None

class AdminCreate(AdminBase):
    pass

class AdminUpdate(AdminBase):
    pass

class AdminResponse(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
