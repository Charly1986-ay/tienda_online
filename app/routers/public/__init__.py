from fastapi import APIRouter

from app.routers.public import index
from app.routers.public import categories

router = APIRouter()

# Incluir subrouters
router.include_router(index.router)
router.include_router(categories.router)