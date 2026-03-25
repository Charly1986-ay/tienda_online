from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.exceptions import CategoryNotFoundException, CategoryBadRequestException
import app.crud.crud_category as crud
from app.schemas.schemas_categories import CategoryCreate, CategoryUpdate
from app.services.pagination import create_pagination

LIMIT = 10


def list_categories_service(
        db: Session, 
        page: int, 
        category=None
):   
    # --- Contar categorias filtrados ---
    count = crud.get_categories_count_filter(
        db=db,
        category=category or None,
    )

    # --- Paginación segura ---
    page, skip, total_pages = create_pagination(page, LIMIT, count)

    # --- Obtener categorias filtradas ---
    categories = crud.get_categories_filter(
        db=db,
        skip=skip,
        limit=LIMIT,
        category=category or None
    )

    return {
        "categories": categories,
        "page": page,
        "total_pages": total_pages,
        "count": count
    } 


def get_all_categories(db: Session):
    try:
        categories = crud.get_all_categories(db)
        if not categories:
            return []  # Devuelve lista vacía si no hay categorías
        return categories
    except Exception as e:
        # Lanza un error 500 si ocurre algún problema en la consulta
        raise HTTPException(status_code=500, detail=f"Error al obtener categorías: {str(e)}")


def get_category_service_by_id(db: Session, id: int):
    category = crud.get_category_by_id(db, id)
    if category  is None:
        raise CategoryNotFoundException()
    
    return category


def create_category_service(db: Session, data: CategoryCreate):
    if crud.get_category_by_name(db, data.name):
        raise CategoryNotFoundException()
    
    return crud.create_category(db=db, data=data)


def update_category_service(db: Session, id: int, data: CategoryUpdate):
    category = crud.get_category_by_id(db, id)
    if not category:
        raise CategoryNotFoundException()
    
    # Verificar que no exista otra categoría con el mismo nombre
    existing = crud.get_category_by_name(db, data.name)    
    if existing and existing.id != id:
        raise CategoryBadRequestException()
    
    return crud.update_category(db, id, data)


def delete_category_services(db: Session, id: int):
    category = crud.get_category_by_id(db, id)
    if category  is None:
        raise CategoryNotFoundException()
    
    crud.delete_category(db, id)