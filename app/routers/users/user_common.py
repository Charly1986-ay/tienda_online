from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jinja_template import templates
from app.dependencies import get_current_user_active
from app.schemas.schemas_users import UserCreate, UserUpdate
import app.services.services_users as services
from app.routers.utils import render_form_errors

router = APIRouter()


@router.get("/profile", name="profile_user")
async def profile(
        request: Request, 
        user = Depends(get_current_user_active)
    ):
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@router.get("/account", name="account_user", response_class=HTMLResponse)
async def account_page(request: Request):
    return templates.TemplateResponse("register_user.html", {
        "request": request,
        "post_action": "/users/register",
        "form_data": {},
        "errors": {}
    })

@router.post("/register")
async def create_cammon_user(
        request: Request, 
        db: Session = Depends(get_db)
    ):
    form = await request.form()
    user_data = UserCreate(**form, role=1)
    try:
        services.create_user_service(db, user_data)
    except ValueError as e:
        return render_form_errors(request, form, e, "register_user.html")
    return RedirectResponse("/auth/login", status_code=302)



@router.get("/edit_profile", name="edit_profile_user")
async def edit_profile_page(request: Request, current_user = Depends(get_current_user_active)):
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": current_user})

@router.post("/update")
async def update_user(
        request: Request, 
        db: Session = Depends(get_db), 
        user = Depends(get_current_user_active)
    ):
    form = await request.form()
    try:
        user_data = UserUpdate(**form)
        services.update_user_service(db, id=user.id, user_data=user_data)
    except ValueError as e:
        return RedirectResponse(f"/users/edit_profile?error={str(e)}", status_code=303)

    return RedirectResponse("/users/profile", status_code=303)