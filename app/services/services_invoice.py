from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.schemas_invoices import InvoiceCreate, OrderCreate
from app.services import services_articles
from app.crud import crud_invoices


def create_invoice_service(db: Session, data: dict, user_id: int):
    if not data.get('items'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No hay items en la compra'
        )

    total = 0

    for item in data['items']:  
        subtotal = item['price'] * item['quantity']          
        total += subtotal

    invoice = InvoiceCreate(customer_id=user_id, total=total)

    invoice_ = crud_invoices.create_invoices(db=db, data=invoice)

    for item in data['items']:            
        order = OrderCreate(            
            article_id=item['id'],
            price=item['price'],
            units=item['quantity'],
            subtotal=item['price'] * item['quantity'],
            invoice_id=invoice_.id
        )

        crud_invoices.create_order(db=db, data=order)

        services_articles.decrece_stock(
            db=db,
            article_id=order.article_id,
            quantity=order.units
        )