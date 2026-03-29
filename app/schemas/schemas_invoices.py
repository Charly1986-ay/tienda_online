from pydantic import BaseModel, model_validator
import datetime


class Invoice(BaseModel):
    customer_id: int
    total: float

class InvoiceResponse(Invoice):
    invoice_id: int
    date_: datetime.datetime

class InvoiceCreate(Invoice):
    pass


class OrderBase(BaseModel):
    article_id: int
    price: float
    units: int
    subtotal: float

class OrderCreate(OrderBase):
    invoice_id: int

class OrderResponse(OrderBase):
    invoice: int    