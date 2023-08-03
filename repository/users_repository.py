from sqlalchemy.orm import Session
import models, security
from schemas import users_schemas


class UsersRepository:
    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user: users_schemas.UserCreate):
        hashed_password = security.get_password_hash(user.password)
        db_user = models.User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = UsersRepository.get_user_by_email(db=db, email=email)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user
