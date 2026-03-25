from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from app.dependencies import get_current_admin_active
from app.core.jinja_template import templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas_categories import CategoryCreate, CategoryResponse, CategoryUpdate
import app.services.services_categories as services
from app.core.exceptions import UnexpectedErrorException

router = APIRouter()


@router.get("", name="admin_categories")
async def list_categories(
    request: Request,
    page: int = Query(1, ge=1),
    category: str = Query("", alias="category"),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin_active)
):
    # Intenta obtener los resultados, si falla devuelve template con lista vacía
    result = {"categories": [], "page": 1, "total_pages": 1, "count": 0}
    error = None

    try:
        result = services.list_categories_service(db=db, page=page, category=category)
    except Exception as e:
        error = str(e)

    return templates.TemplateResponse(
        "admin_categories.html",
        {
            "request": request,
            "admin": admin,
            "categories": result["categories"],
            "page": result["page"],
            "total_pages": result["total_pages"],
            "count": result["count"],
            "filters": {"category": category},
            "error": error
        }
    )



@router.get("/combo", response_model=list[CategoryResponse], name="admin_categories_all")
async def get_combo_categorie(
    request: Request,    
    db: Session = Depends(get_db),  
    admin = Depends(get_current_admin_active)
):
    return services.get_all_categories(db)


@router.get('/{id}')
def get_category_by_id(    
    id: int,
    db: Session = Depends(get_db),  
    admin = Depends(get_current_admin_active)
):
    return services.get_category_service_by_id(db, id)


@router.post('')
async def create_category(
        request: Request, 
        db: Session = Depends(get_db),  
        admin = Depends(get_current_admin_active)
):
    
    # Leer JSON enviado por fetch
    data = await request.json()
    name = data.get("name", "").strip()

    if not name:
        return JSONResponse({"detail": "El nombre es obligatorio"}, status_code=400)

    # Crear el modelo internamente
    category_data = CategoryCreate(name=name)

    try:
        services.create_category_service(db, category_data)
    except ValueError as e:
        return UnexpectedErrorException()

    return RedirectResponse("/admin/categories", status_code=302)


@router.put('/{id}', response_model=CategoryResponse)
async def update_category(
        id: int,
        request: Request, 
        db: Session = Depends(get_db),  
        admin = Depends(get_current_admin_active)
):
    
    # Leer JSON enviado por fetch
    data = await request.json()
    name = data.get("name", "").strip()

    # Crear el modelo internamente
    category_data = CategoryUpdate(name=name)

    return services.update_category_service(db, id, category_data)


@router.delete('/{id}')
async def delete(
    id: int,
    db: Session = Depends(get_db),  
    admin = Depends(get_current_admin_active)
):
    services.delete_category_services(db, id)