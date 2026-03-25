# app/public/__init__.py
from fastapi import APIRouter
from app.routers.admin.articles import router as articles_router
from app.routers.admin.categories import router as categories_router

router = APIRouter(redirect_slashes=False)
router.include_router(articles_router, prefix="/articles")
router.include_router(categories_router, prefix="/categories")