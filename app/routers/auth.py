from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.jinja_template import templates
from app.schemas.schemas_users import UserLogin
import app.services.services_auth as services


router = APIRouter()


@router.get("/login", name="login_user")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request})


@router.post("/token")
async def login(
        request: Request, db: 
        Session = Depends(get_db)
    ):
    form = await request.form()
    user_data = UserLogin(**form)

    try:
        result = services.login_service(db, user_data)
    except ValueError:
        return RedirectResponse("/auth/login", status_code=303)  

    # Redirección según rol
    if result["role"] == 2:
        redirect_url = "/admin/articles"
        #redirect_url = "/admin/articles/search"
    else:
        redirect_url = "/users/profile"

    response = RedirectResponse(url=redirect_url, status_code=303)

    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        max_age=services.ACCESS_TOKEN_EXPIRE_SECONS * 60,
        httponly=True,
        secure=True,       # En desarrolo => secure=False, en producción secure=True
        samesite="lax",
        path="/"
    )
    return response


@router.post("/logout")
async def logout():
    response = RedirectResponse(
        "/", 
        status_code=303, 
        headers={'set-cookie': 'access_token=; Max-Age=0'})      

    return response