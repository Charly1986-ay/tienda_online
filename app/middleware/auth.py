from fastapi import Request
from fastapi.responses import RedirectResponse
from app.services.tokens import verify_access_token
from app.core.jinja_template import templates

# Rutas que requieren autenticación
PROTECTED_PATHS = (
    "/users/profile",
    "/users/edit_profile",
    "/users/update",
    "/buy"
)

PROTECTED_PREFIXES = (
    "/admin",
)

async def auth_middleware(request: Request, call_next):
    path = request.url.path
    request.state.user_id = None  # Por defecto no hay usuario

    # Solo validar token en rutas protegidas
    if path.startswith(PROTECTED_PREFIXES) or path in PROTECTED_PATHS:
        token = request.cookies.get("access_token")

        if token:
            try:
                payload = verify_access_token(token)                
                if payload and "sub" in payload:
                    # Guardamos el user_id en request.state
                    request.state.user_id = int(payload["sub"])
            except Exception:
                pass
            
        # Si no hay usuario válido → redirigir a login
        if not request.state.user_id:
            return RedirectResponse(url="/auth/login", status_code=303)

    
    # Continuar con la petición    
    response = await call_next(request)
    
    # Manejo de rutas no encontradas    
    if response.status_code == 404:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )

    return response