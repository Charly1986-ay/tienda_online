from datetime import timedelta
from sqlalchemy.orm import Session
import app.crud.crud_users as crud
from app.schemas.schemas_users import UserLogin
from app.services.tokens import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_SECONS


def login_service(db: Session, user_data: UserLogin):
    user = crud.get_user_by_email(db, user_data.email)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise ValueError("Credenciales no verificadas")    
    
    access_token = create_access_token(
        {"sub": user.id},       
        expires_delta=timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONS * 60)
    )

    return {
        "access_token": access_token,
        "role": user.role
    }