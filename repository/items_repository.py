from sqlalchemy.orm import Session
import models
from schemas import items_schemas


class ItemsRepository:
    @staticmethod
    def get_items(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Item).offset(skip).limit(limit).all()

    @staticmethod
    def create_user_item(db: Session, item: items_schemas.ItemCreate, user_id: int):
        db_item = models.Item(**item.dict(), owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
