from fastapi import APIRouter
from app.routers.public import router as public_router
from app.routers.admin import router as admin_router
from app.routers import auth as auth_router
from app.routers.users import router as users_router


router = APIRouter()
router.include_router(public_router)
router.include_router(users_router)
router.include_router(admin_router, prefix="/admin")
router.include_router(auth_router.router, prefix="/auth")