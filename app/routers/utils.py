from fastapi import Request
from app.core.jinja_template import templates


def render_form_errors(request: Request, form: dict, error: Exception, template_name: str):
    """
    Devuelve un TemplateResponse con los errores mapeados y los datos del formulario preservados.
    """
    error_map = {
        "password_mismatch": "repeat_password",
        "username_taken": "username",
        "email_taken": "email"
    }
    
    field = error_map.get(str(error), "__root__")
    errors = {field: [str(error)]}
    
    form_data_preserved = {
        "username": form.get("username", ""),
        "full_name": form.get("full_name", ""),
        "email": form.get("email", "")
    }
    
    return templates.TemplateResponse(
        template_name,
        {
            "request": request,
            "form_data": form_data_preserved,
            "errors": errors
        }
    )
