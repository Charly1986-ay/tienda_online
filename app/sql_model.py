from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, DateTime
#from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List


# ===========================
# MODELO USER
# ===========================
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)

    articles: Mapped[List["Article"]] = relationship(back_populates="user")
    invoices: Mapped[List["Invoice"]] = relationship(back_populates="customer")


# ===========================
# MODELO CATEGORY
# ===========================
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    articles: Mapped[List["Article"]] = relationship(back_populates="category")


# ===========================
# MODELO ARTICLE
# ===========================
class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Foreign Keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)    

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="articles")
    category: Mapped["Category"] = relationship(back_populates="articles")
    orders: Mapped[List["Order"]] = relationship(back_populates="article")
    invoices: Mapped[List["Invoice"]] = relationship(
        secondary="orders",
        back_populates="articles",
        viewonly=True
    )


# ===========================
# MODELO INVOICE
# ===========================
class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    total: Mapped[float] = mapped_column(Float, nullable=False)

    # Relaciones
    customer: Mapped["User"] = relationship(back_populates="invoices")
    orders: Mapped[List["Order"]] = relationship(back_populates="invoice")
    articles: Mapped[List["Article"]] = relationship(
        secondary="orders",
        back_populates="invoices",
        viewonly=True
    )


# ===========================
# MODELO ORDER (intermedia)
# ===========================
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), nullable=False)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False)

    price: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)

    article: Mapped["Article"] = relationship(back_populates="orders")
    invoice: Mapped["Invoice"] = relationship(back_populates="orders")