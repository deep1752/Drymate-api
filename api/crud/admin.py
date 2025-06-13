from sqlalchemy.orm import Session
from api.database.models import admin as models
from api.database.schemas import admin as schemas

def get_all_admins(db: Session):
    return db.query(models.Admin).all()

def get_admin_by_id(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Admin.id == admin_id).first()

def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(**admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def update_admin(db: Session, admin_id: int, admin_update: schemas.AdminUpdate):
    db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if db_admin:
        for key, value in admin_update.dict().items():
            setattr(db_admin, key, value)
        db.commit()
        db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, admin_id: int):
    db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if db_admin:
        db.delete(db_admin)
        db.commit()
    return db_admin
