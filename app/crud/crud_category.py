from sqlalchemy.orm import Session
from app.sql_model import Category
from app.schemas.schemas_categories import CategoryCreate, CategoryUpdate


# ====== Consultas ======

def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def get_categories(db: Session, skip: int, limit: int):
    return db.query(Category).offset(skip).limit(limit).all()


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_categories_count(db: Session):
    return db.query(Category).count()


def get_categories_count_filter(db: Session, category=None):
    query = db.query(Category)
    
    if category:
        query = query.filter(Category.name.ilike(f"%{category}%"))    

    return query.count()


def get_categories_filter(db: Session, skip: int, limit: int, category=None):
    query = db.query(Category)
    
    if category:
        query = query.filter(Category.name.ilike(f"%{category}%"))

    return query.offset(skip).limit(limit).all()


# ====== Crear categoria ======

def create_category(db: Session, data: CategoryCreate):
    db_category = Category(
        name = data.name
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# ====== Actualizar categoria ======

def update_category(db: Session, id: int, data: CategoryUpdate):

    db_category = db.query(Category).filter(Category.id == id).first()

    if not db_category:
        return None

    update_data = data.model_dump(exclude_unset=True)

    # Solo actualizar si el campo está presente en la request
    for key, value in update_data.items():        
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)

    return db_category


def delete_category(db: Session, id: int):
    category = db.get(Category, id)

    if not category:
        return None

    db.delete(category)
    db.commit()