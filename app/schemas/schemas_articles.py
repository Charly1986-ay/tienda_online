from typing import Optional
from pydantic import BaseModel


class ArticleBase(BaseModel):
    name: str
    description: str
    categorie_id: int  # Usamos solo el id de la categoría
    stock: int
    price: float
    imagen: str


class ArticleCreate(ArticleBase):
    admin_id: int


class ArticleUpdate(ArticleBase):
    name: Optional[str] = None
    description: Optional[str] = None
    categorie_id: Optional[int] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    image: Optional[str] = None


class CategoryResponse(ArticleBase):
    id: int

    model_config = {
        "from_attributes": True
    }