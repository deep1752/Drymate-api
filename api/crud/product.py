from sqlalchemy.orm import Session
from api.database.models.product import Product
from api.database.schemas.product import ProductCreate, ProductUpdate

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductCreate, image_path: str = None):
    db_product = Product(**product.dict(), image=image_path)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate, image_path: str = None):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None
    for field, value in product.dict().items():
        setattr(db_product, field, value)
    if image_path:
        db_product.image = image_path
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
