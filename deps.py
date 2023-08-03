from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
import models, security
from database import SessionLocal
from settings import Settings
from schemas import users_schemas
from repository.users_repository import UsersRepository

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
):
    try:
        payload = jwt.decode(
            token, Settings.secret_key, algorithms=[security.ALGORITHM]
        )
        token_data = users_schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = UsersRepository.get_user(db, user_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_superuser(current_user: models.User = Depends(get_current_user)):
    if not current_user.email == Settings.super_user_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not the superuser"
        )
    return current_user
