from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from api.database.connection import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    final_price = Column(Float, nullable=False)
    discripction = Column(String(255), nullable=False)
    status = Column(String(50), default="active")
    image = Column(String(255), nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
