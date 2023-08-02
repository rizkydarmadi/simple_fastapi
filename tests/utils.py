from sqlalchemy.orm import Session
from .. import models, security
from ..settings import settings
from repository.users_repository import UsersRepository
from schemas import users_schemas


def get_superuser_access_token(db: Session):
    superuser = UsersRepository.get_user_by_email(db, email=settings.super_user_email)
    return get_user_access_token(superuser)


def get_token_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


def get_user_access_token(user: models.User):
    return security.create_access_token(subject=user.id)


def create_test_user(db: Session):
    user_in = users_schemas.UserCreate(
        email="test@example.com", password="examplesecret"
    )
    return UsersRepository.create_user(db, user=user_in)
