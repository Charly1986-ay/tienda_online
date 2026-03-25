from fastapi import APIRouter
from app.routers.users import user_admin, user_common

router = APIRouter(redirect_slashes=False)
router.include_router(user_common.router, prefix="/users",  tags=["users"])
router.include_router(user_admin.router, prefix="/admin/users", tags=["admin_users"])