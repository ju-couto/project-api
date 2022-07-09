from sqlalchemy.orm import Session

from . import models, schemas


class UserRepo:
    async def create(db: Session, user: schemas.User):
        db_user = models.User(username=user.username, hash_password=user.hash_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def fetch_by_id(db: Session,_id):
        return db.query(models.User).filter(models.User.id == _id).first()

    def fetch_by_username(db: Session,username):
        return db.query(models.User).filter(models.User.username == username).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    async def delete(db: Session,user_id):
        db_user = db.query(models.User).filter_by(id=user_id).first()
        db.delete(db_user)
        db.commit()

    async def update(db: Session, user_data):
        updated_user = db.merge(user_data)
        db.commit()
        return updated_user


