from sqlalchemy.orm import Session, joinedload
from app.schemas.schemas_invoices import OrderCreate
from app.sql_model import Invoice, Order
from app.schemas.schemas_invoices import InvoiceCreate

from datetime import datetime, timedelta


# ====== Consultas ======
def get_invoices_by_id(db: Session, id: int):
    return db.query(Invoice).filter(Invoice.id == id).first()


def get_invoices_by_id(db: Session, customer_id: int):
    return db.query(Invoice).filter(Invoice.customer_id == customer_id).all()


def get_invoices_by_date(db: Session, date: datetime):

    next_day = date + timedelta(days=1)

    return (
        db.query(Invoice)
        .filter(
            Invoice.date >= date,
            Invoice.date < next_day
        )
        .all()
    )


def create_invoices(db: Session, data: InvoiceCreate):   
    db_invoice = Invoice(        
        customer_id = data.customer_id,        
        total = data.total
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


# =================================================================================

def get_order_by_id(db: Session, id: int):
    return db.query(Order).filter(Order.id == id).first()


def get_order_by_invoice(db: Session, invoice_id: int):
    return db.query(Order).filter(Order.invoice_id == invoice_id).all()


def create_order(db: Session, data: OrderCreate):   
    db_order = Order(        
        article_id = data.article_id,  
        invoice_id = data.invoice_id,      
        price = data.price,
        unit = data.units,
        subtotal = data.subtotal
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order