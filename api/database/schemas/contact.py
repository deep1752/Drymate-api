from pydantic import BaseModel, EmailStr

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactResponse(ContactCreate):
    id: int

    class Config:
        from_attributes = True
