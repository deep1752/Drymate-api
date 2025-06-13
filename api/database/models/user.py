from sqlalchemy import Column, Integer, String, DateTime, func
from api.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    mobile = Column(String(15), unique=True, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    role = Column(String(20), default="customer")  # Default role set to 'customer'
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, nullable=True)
