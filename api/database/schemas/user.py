from pydantic import BaseModel, EmailStr,validator
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    mobile: str
    age: Optional[int] = None
    gender: Optional[str] = None

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    mobile: Optional[str]
    age: Optional[int]
    gender: Optional[str]

class PasswordUpdate(BaseModel):
  
    new_password: str
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    age: Optional[int] = None
    gender: Optional[str] = None
    role: str  # Include role in the response

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
