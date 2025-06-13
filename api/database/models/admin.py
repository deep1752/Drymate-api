from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from api.database.connection import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    mobile_number = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    twiter_link = Column(String(255), nullable=True)
    linkedin_link = Column(String(255), nullable=True)
    fb_link = Column(String(255), nullable=True)
    insta_link = Column(String(255), nullable=True)
    youtube_link = Column(String(255), nullable=True)
    expirence_in_year = Column(Integer, nullable=True)
    complet_project_numbers = Column(Integer, nullable=True)
    happy_clint_numbers = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
