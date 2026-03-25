from sqlalchemy.orm import Session
import app.crud.crud_users as crud
from app.schemas.schemas_users import UserCreate, UserUpdate
from app.services.pagination import create_pagination
from app.services.tokens import get_password_hash
from app.core.exceptions import UserNotFoundException

LIMIT = 5

def list_users_services(
        db: Session, 
        page: int, 
        username=None, 
        full_name=None, 
        email=None, 
        role=None, 
        disabled=None
):
    # --- Lógica de negocio: convertir filtros ---
    role_map = {"user": 1, "admin": 2}
    if role:
        try:
            role_int = int(role)  # si viene "2" o "1"
        except ValueError:
            role_int = role_map.get(role)
    else:
        role_int = None

    if disabled is not None and isinstance(disabled, str):
        disabled_bool = disabled.lower() == "true"
    else:
        disabled_bool = disabled

    # --- Contar usuarios filtrados ---
    count = crud.get_users_count_filter(
        db=db,
        username=username or None,
        full_name=full_name or None,
        email=email or None,
        role=role_int,
        disabled=disabled_bool
    )

    # --- Paginación segura ---
    page, skip, total_pages = create_pagination(page, LIMIT, count)

    # --- Obtener usuarios filtrados ---
    users = crud.get_users_filter(
        db=db,
        skip=skip,
        limit=LIMIT,
        username=username or None,
        full_name=full_name or None,
        email=email or None,
        role=role_int,
        disabled=disabled_bool
    )

    return {
        "users": users,
        "page": page,
        "total_pages": total_pages,
        "count": count
    }    


def get_service_user_by_id(db: Session, id: int):
    user = crud.get_user_by_id(db=db, user_id=id)
    if user  is None:
        raise UserNotFoundException()    
    return user


def create_user_service(db: Session, user_data: UserCreate):
    # 1. Verificar que passwords coincidan
    if user_data.password != user_data.repeat_password:
        raise ValueError("password_mismatch")

    # 2. Verificar unicidad de username
    if crud.get_user_by_username(db, user_data.username):
        raise ValueError("username_taken")
    
    # 3. Verificar unicidad de email
    if crud.get_user_by_email(db, user_data.email):
        raise ValueError("email_taken")
    
    # 4. Hashear la contraseña
    hashed = get_password_hash(user_data.password)
    user_data.password = hashed
    # 5. Crear usuario en DB
    return crud.create_user(db, user_data)


def update_user_service(db: Session, id: int, user_data: UserUpdate):

    db_user = crud.get_user_by_id(db, id)
    if not db_user:
        raise ValueError("not_found")

    # Validación de unicidad para username
    existing_user = crud.get_user_by_username(db, user_data.username)
    if existing_user and existing_user.id != id:
        raise ValueError("username_taken")

    # Validación de unicidad para email
    existing_email_user = crud.get_user_by_email(db, user_data.email)
    if existing_email_user and existing_email_user.id != id:
        raise ValueError("email_taken")

    # Manejo del password
    if user_data.password:  # usuario quiere cambiar contraseña
        if user_data.password != user_data.repeat_password:
            raise ValueError("password_mismatch")

        user_data.password = get_password_hash(user_data.password)
    else:
        # Usuario no cambió contraseña
        user_data.password = None
    return crud.update_user(db, id, user_data)


def desactivate_account(db: Session, id: int):
    db_user = crud.get_user_by_id(db, id)
    if not db_user:
        raise ValueError("not_found")
    
    return crud.desactivate_user(db, id)