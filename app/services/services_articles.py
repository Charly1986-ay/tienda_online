import os
import uuid
from dotenv import load_dotenv
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.crud import crud_articles as crud
from app.schemas.schemas_articles import ArticleCreate, ArticleUpdate
from app.services.pagination import create_pagination
from app.core.exceptions import ProductExistException, ProductNotFoundException, ProductStockException
from app.crud import crud_articles as crud

load_dotenv()  # Cargar variables de .env

PATH_IMG = os.getenv("PATH_IMG")
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png"]
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB


def list_articles_services(db: Session, page: int, limit:int, name=None, category=None, available=None):
    # Contar artículos filtrados
    count = crud.get_articles_count_filter(db, name, category, available)

    # Paginar
    page, skip, total_pages = create_pagination(page, limit, count)

    # Obtener artículos filtrados
    articles = crud.get_articles_filter(
        db, skip=skip, limit=limit, name=name, category=category, available=available
    )

    return {
        "articles": articles,
        "page": page,
        "total_pages": total_pages,
        "count": count
    }


def suggestions_articles_services(db: Session, limit:int, name=None):
    articles = crud.get_all_articles_by_name(db, name)
    return [a.name for a in articles[:limit]]



def get_service_article_by_id(db: Session, id: int):
    article = crud.get_article_by_id(db, id)
    if article  is None:
        raise ProductNotFoundException()
    
    return article



def create_article_service(db: Session, data: dict):
    # 1. Validar si ya existe
    if crud.get_article_by_name(db, data["name"]):
        raise ProductExistException()

    # 2. Guardar imagen si viene, si no usar default
    image_file: UploadFile = data.get("imagen")    

    # renombra la imagen
    data['imagen'] = name_image(image_file=image_file)

    # 3. Crear Pydantic y guardar en DB
    article = ArticleCreate(**data)
    return crud.create_article(db, article)



def update_article_service(db: Session, id: int, data: dict):   
    existing_article = crud.get_article_by_id(db, id)
    if not existing_article:
        raise ProductNotFoundException()

    existing = crud.get_article_by_name(db, data["name"])
    if existing and existing.id != id:
        raise ProductExistException()   
    
    # 2. Guardar imagen si viene, si no usar default
    image_file: UploadFile = data.get("imagen")
    
    data['imagen'] = image_file
    
    article = ArticleUpdate(**data)

    return crud.update_article(db, id, article)



def save_article_image(image_file: UploadFile) -> str:
    ext = os.path.splitext(image_file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Solo se permiten imágenes JPG, JPEG o PNG")

    # Validar tamaño
    image_file.file.seek(0, 2)
    size = image_file.file.tell()
    image_file.file.seek(0)
    if size > MAX_IMAGE_SIZE:
        raise ValueError("La imagen no puede superar los 10 MB")

    # name único
    image_name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(PATH_IMG, image_name)

    with open(path, "wb") as f:
        f.write(image_file.file.read())

    return image_name



def name_image(image_file: UploadFile):
    if image_file and getattr(image_file, "filename", None):
        image_name = save_article_image(image_file)
    else:
        image_name = "default.png"  # archivo físico que debe existir en /static/img
    return image_name



def decrece_stock(db: Session, article_id: int, quantity: int):
    article = crud.get_article_by_id(db=db, article_id=article_id)

    if article.stock < quantity:
        raise ProductStockException()
    
    data = ArticleUpdate(**article)
    
    return crud.update_article(db=db, id=article_id, data=data)