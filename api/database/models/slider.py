from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from api.database.connection import Base

class StatusEnum(PyEnum):
    active = "active"
    inactive = "inactive"

class Slider(Base):
    __tablename__ = "sliders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255), nullable=False)
    image = Column(String(255), nullable=False)  # Store image path
    status = Column(Enum(StatusEnum), default=StatusEnum.active)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


