from sqlalchemy import Column, Integer, String, Text
from api.database.connection import get_db
from api.database.connection import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    subject = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)


