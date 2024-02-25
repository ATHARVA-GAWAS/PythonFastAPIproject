from sqlalchemy.orm import Session
from typing import List
from . import models

def create_item(db: Session, item: models.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 10) -> List[models.Item]:
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_items(db: Session, skip: int = 0, limit: int = 10) -> List[models.Item]:
    return db.query(models.Item).offset(skip).limit(limit).all()

def update_item(db: Session, item_id: int, item: models.ItemCreate):
    db_item = get_items(db, item_id)
    if db_item:
        for attr, value in item.dict().items():
            setattr(db_item, attr, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_items(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
