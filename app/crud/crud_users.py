from sqlalchemy.orm import Session
from app.sql_model import User
from app.schemas.schemas_users import UserCreate, UserUpdate
from sqlalchemy.orm import joinedload


# ====== Consultas ======

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_role(db: Session, role: int):
    return db.query(User).filter(User.role == role).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


# crud.py
def get_users_count_filter(db: Session, username=None, full_name=None, email=None, role=None, disabled=None):
    query = db.query(User)
    
    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))
    if full_name:
        query = query.filter(User.full_name.ilike(f"%{full_name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if role is not None:
        query = query.filter(User.role == role)
    if disabled is not None:
        query = query.filter(User.disabled == disabled)

    return query.count()


def get_users_filter(db: Session, skip: int, limit: int, username=None, full_name=None, email=None, role=None, disabled=None):
    query = db.query(User)
    
    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))
    if full_name:
        query = query.filter(User.full_name.ilike(f"%{full_name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if role is not None:
        query = query.filter(User.role == role)
    if disabled is not None:
        query = query.filter(User.disabled == disabled)

    return query.offset(skip).limit(limit).all()


# ====== Crear usuario ======

def create_user(db: Session, data: UserCreate):
    db_user = User(
        username=data.username,
        full_name=data.full_name,
        email=data.email,
        hashed_password=data.password,
        role=data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ====== Actualizar usuario ======

def update_user(db: Session, id: int, data: UserUpdate):

    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():

        # Nunca actualizar repeat_password
        if key == "repeat_password":
            continue

        # Si password es None → significa "NO cambiar la contraseña"
        if key == "password" and value is None:
            continue

        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def desactivate_user(db: Session, id: int):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        return None

    db_user.disabled = True

    db.commit()
    db.refresh(db_user)

    return db_user