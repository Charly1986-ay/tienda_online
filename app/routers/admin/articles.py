from fastapi import APIRouter, Depends, Query, Request, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.exceptions import ProductExistException
from app.services import services_articles as services
from app.core.database import get_db
from app.dependencies import get_current_admin_active
from app.core.jinja_template import templates

router = APIRouter()

LIMIT = 8

@router.get("", name="admin_articles")
async def list_articles(
    request: Request,
    page: int = Query(1, ge=1),
    name: str = Query("", alias="name"),
    category: str = Query("", alias="category"),
    available: str = Query("", alias="available"),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin_active)
):
    # Convertir filtros
    available_bool = None
    if available.lower() == "true":
        available_bool = True
    elif available.lower() == "false":
        available_bool = False

    category_id = int(category) if category else None

    # Llamar al servicio
    result = services.list_articles_services(
        db=db,
        page=page,
        limit=LIMIT,
        name=name or None,
        category=category_id,
        available=available_bool        
    )

    filters = {"name": name, "category": category, "available": available}

    return templates.TemplateResponse(
        "admin_articles.html",
        {
            "request": request,
            "admin": admin,
            "articles": result["articles"],
            "page": result["page"],
            "total_pages": result["total_pages"],
            "count": result["count"],
            "filters": filters
        }
    )


@router.get('/{id}')
def get_article_by_id(    
    id: int,
    db: Session = Depends(get_db),  
    admin = Depends(get_current_admin_active)
):
    return services.get_service_article_by_id(db, id)


@router.post('')
async def create_article(
        request: Request, 
        db: Session = Depends(get_db),  
        admin = Depends(get_current_admin_active)
):    
    form = await request.form()
    image: UploadFile = form.get("productImg")
    data = parse_article_form(form, image, admin.id)

    try:
        services.create_article_service(db, data)
    except ProductExistException:
        return JSONResponse({"msg": "Ya existe un producto con ese name"}, status_code=409)
    
    except Exception:
        return JSONResponse({"msg": "Error inesperado"}, status_code=500)
    
    return JSONResponse({"msg": "Artículo guardado correctamente"})


@router.put('/{id}')
async def update_article(
        id: int,
        request: Request, 
        db: Session = Depends(get_db),  
        admin = Depends(get_current_admin_active)
):    
    form = await request.form()
    image: UploadFile = form.get("productImg")     
    data = parse_article_form(form, image, admin.id)

    try:
        services.update_article_service(db, id, data)
    except ProductExistException:
        return JSONResponse({"msg": "Ya existe un producto con ese name"}, status_code=409)
    except Exception:
        return JSONResponse({"msg": "Error inesperado"}, status_code=500)

    return JSONResponse({"msg": "Artículo guardado correctamente"})


def parse_article_form(form, image, admin_id):
    return {
        "name": form.get("productName"),
        "description": form.get("productDesc"),
        "categorie_id": int(form.get("productCategory")),  # Aquí estamos obteniendo el ID de la categoría
        "stock": int(form.get("productQty")),
        "price": float(form.get("productPrice")),
        "imagen": image,
        "admin_id": admin_id
    }