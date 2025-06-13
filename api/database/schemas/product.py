from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: float
    discount: Optional[float] = 0.0
    final_price: float
    discripction: str
    status: Optional[str] = "active"

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    image: Optional[str]
    created: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

