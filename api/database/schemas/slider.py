from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"

class SliderBase(BaseModel):
    title: str
    subtitle: str
    status: StatusEnum

class SliderCreate(SliderBase):
    pass

class SliderUpdate(SliderBase):
    pass

class SliderOut(SliderBase):
    id: int
    image: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True

