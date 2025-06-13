from sqlalchemy.orm import Session
from api.database.models.contact import Contact
from api.database.schemas.contact import ContactCreate

def create_contact(db: Session, contact_data: ContactCreate):
    contact = Contact(**contact_data.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
