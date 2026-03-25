from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import services_categories as services

router = APIRouter()

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = services.get_all_categories(db)
    return {"categories": categories}