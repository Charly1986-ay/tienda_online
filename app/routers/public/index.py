import datetime
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.dependencies import get_current_user_active
from app.services import services_articles 
from app.services import services_invoice
from app.core.database import get_db
from app.core.jinja_template import templates

router = APIRouter()

LIMIT = 8

@router.get("/", name="index_page")
async def index(
    request: Request,
    page: int = Query(1, ge=1),
    name: str = Query("", alias="name"),
    category: str = Query("", alias="category"),    
    db: Session = Depends(get_db),    
):    
    result = services_articles.list_articles_services(
        db=db,
        page=page,
        limit=LIMIT,
        name=name or None,
        category=category or None,        
        available=None
    )

    filters = {"name": name, "category": None, "available": None}

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,           
            "articles": result["articles"],
            "page": result["page"],
            "total_pages": result["total_pages"],
            "count": result["count"],
            "filters": filters
        }
    )



@router.get("/search-suggestions", name="search-suggestions")
async def search_suggestions(
    request: Request,   
    q: str = Query("", min_length=1),    
    db: Session = Depends(get_db),    
):    
    result = services_articles.suggestions_articles_services(
        db=db,        
        limit=LIMIT,
        name=q or None        
    )

    return result



@router.get("/articles")
def load_more_articles(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    result = services_articles.list_articles_services(
        db=db,
        page=page,
        name=None,
        category=None,
        available=None,
        limit=LIMIT
    )

    return {
        "articles": result["articles"],
        "page": result["page"],
        "total_pages": result["total_pages"]
    }



@router.get("/articles/{product_id}")
async def product_detail(
    request: Request, 
    product_id: int,
    db: Session = Depends(get_db)
):
    product = services_articles.get_service_article_by_id(db=db, id=product_id)

    return templates.TemplateResponse(
        "view_product.html",
        {
            "request": request,
            "product": product
        }
    )



@router.post("/buy")
async def buy(
    request: Request, 
    db: Session = Depends(get_db),
    user = Depends(get_current_user_active)
):    
    data = await request.json()
    #print(type(data))
    services_invoice.create_invoice_service(db=db, data=data, user_id=user.id)  

    return {"message": "Compra realizada correctamente"}


@router.get("/get_current_year")
async def get_current_year():    
    return {"current_year": f'{datetime.datetime.now().year}'}     