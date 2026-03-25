from fastapi import APIRouter, Query, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jinja_template import templates
from app.dependencies import get_current_admin_active
from app.routers.utils import render_form_errors
from app.schemas.schemas_users import UserCreate, UserUpdate
import app.services.services_users as services


router = APIRouter()


@router.get("", name="admin_users")
async def list_users(
    request: Request,
    page: int = Query(1, ge=1),
    username: str = Query("", alias="username"),
    fullname: str = Query("", alias="fullname"),
    email: str = Query("", alias="email"),
    role: str = Query("", alias="role"),
    disabled: str = Query("", alias="disabled"),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin_active)
):
    result = services.list_users_services(
        db=db,
        page=page,
        username=username,
        full_name=fullname,
        email=email,
        role=role,
        disabled=disabled
    )

    filters = {
        "username": username,
        "fullname": fullname,
        "email": email,
        "role": role,
        "disabled": disabled
    }

    return templates.TemplateResponse("admin_users.html", {
        "request": request,
        "admin": admin,
        "users": result["users"],
        "page": result["page"],
        "total_pages": result["total_pages"],
        "count": result["count"],
        "filters": filters
    })


@router.get('/{id}')
def get_user_by_id(    
    id: int,
    db: Session = Depends(get_db),  
    admin = Depends(get_current_admin_active)
):
    return services.get_service_user_by_id(db=db, id=id)


@router.post("")
async def create_admin(
    request: Request, 
    db: Session = Depends(get_db)
):
    data = await request.json()
    try:
        user_data = UserCreate(**data, role=2)
        user = services.create_user_service(db, user_data)
        return {
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email
            }
        }
    except ValueError as e:
        return {"success": False, "errors": str(e)}    
    

@router.post("/{id}")
async def update_admin(request: Request, id: int, db: Session = Depends(get_db)):
    data = await request.json()
    try:
        user_data = UserUpdate(**data)
        updated_user = services.update_user_service(db, id=id, user_data=user_data)
        return {
            "success": True,
            "user": {
                "id": updated_user.id,
                "username": updated_user.username,
                "full_name": updated_user.full_name,
                "email": updated_user.email
            }
        }
    except ValueError as e:
        return {"success": False, "errors": str(e)}