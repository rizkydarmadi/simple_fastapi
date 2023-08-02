from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import deps, models, security
from .api import items, users
from .database import SessionLocal, engine
from .settings import settings
from repository.users_repository import UsersRepository
from schemas import users_schemas

app = FastAPI()

app.include_router(users.router, tags=["users"])
app.include_router(items.router, tags=["items"])


@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    user = UsersRepository.get_user_by_email(db, settings.super_user_email)
    if not user:
        user_in = users_schemas.UserCreate(
            email=settings.super_user_email, password=settings.super_user_password
        )
        UsersRepository.create_user(db, user_in)
    db.close()


@app.post("/login/access-token", response_model=users_schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = UsersRepository.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {
        "access_token": security.create_access_token(subject=user.id),
        "token_type": "bearer",
    }
