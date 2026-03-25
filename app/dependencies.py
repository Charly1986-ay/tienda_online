from fastapi import Depends, Request
from app.core.database import get_db
from app.crud.crud_users import get_user_by_id
from app.core.exceptions import CredentialsException, UserInactiveException


def get_token_user_id(request: Request):
    user_id = request.state.user_id
    if not user_id:
        raise CredentialsException()
    return user_id


def get_current_user(user_id: int = Depends(get_token_user_id), db = Depends(get_db)):
   
    user = get_user_by_id(db, user_id)
    if not user:
        raise CredentialsException()
    return user


def get_current_user_active(user = Depends(get_current_user)):
    
    if user.disabled:
        raise UserInactiveException()
    return user


def get_current_admin(user_id: int = Depends(get_token_user_id), db = Depends(get_db)):
   
    user = get_user_by_id(db, user_id)
    if not user:
        raise CredentialsException()    
    
    if user.role != 2:
        raise CredentialsException()
    return user


def get_current_admin_active(user = Depends(get_current_admin)):
    
    if user.disabled:
        raise UserInactiveException()
    return user