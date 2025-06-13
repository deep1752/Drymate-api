# crud/trainer.py
from sqlalchemy.orm import Session
from api.database.models.trainer import Trainer
from api.database.schemas.trainer import TrainerCreate, TrainerUpdate

def create_trainer(db: Session, trainer: TrainerCreate):
    db_trainer = Trainer(**trainer.dict())
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer

def get_all_trainers(db: Session):
    return db.query(Trainer).all()

def get_trainer_by_id(db: Session, trainer_id: int):
    return db.query(Trainer).filter(Trainer.id == trainer_id).first()

def update_trainer(db: Session, trainer_id: int, updated_data: TrainerUpdate):
    db_trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    if not db_trainer:
        return None
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(db_trainer, key, value)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer

def delete_trainer(db: Session, trainer_id: int):
    db_trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    if db_trainer:
        db.delete(db_trainer)
        db.commit()
        return True
    return False
