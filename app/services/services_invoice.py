from sqlalchemy.orm import Session
from app.crud import crud_invoces as crud
from app.services import services_articles

def create_invoice_service(db: Session, data: dict):
    print(data['items'])