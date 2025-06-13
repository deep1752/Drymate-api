from sqlalchemy.orm import Session
from api.database.models.slider import Slider
from api.database.schemas.slider import SliderCreate, SliderUpdate

def create_slider(db: Session, slider_data: SliderCreate, image_path: str):
    slider = Slider(**slider_data.dict(), image=image_path)
    db.add(slider)
    db.commit()
    db.refresh(slider)
    return slider

def get_sliders(db: Session):
    return db.query(Slider).all()

def get_slider(db: Session, slider_id: int):
    return db.query(Slider).filter(Slider.id == slider_id).first()

def update_slider(db: Session, slider_id: int, slider_data: SliderUpdate, image_path: str | None = None):
    slider = get_slider(db, slider_id)
    if not slider:
        return None
    for key, value in slider_data.dict().items():
        setattr(slider, key, value)
    if image_path:
        slider.image = image_path
    db.commit()
    db.refresh(slider)
    return slider

def delete_slider(db: Session, slider_id: int):
    slider = get_slider(db, slider_id)
    if not slider:
        return False
    db.delete(slider)
    db.commit()
    return True
