# models/trainer.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from api.database.connection import Base

class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    designation = Column(String(100), nullable=False)
    mobile_number = Column(String(15), nullable=False)
    twitter_link = Column(String(255))
    fb_link = Column(String(255))
    linkedin_link = Column(String(255))
    image = Column(String(255))  # File path instead of binary
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
