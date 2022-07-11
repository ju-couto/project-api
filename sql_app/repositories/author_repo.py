from sqlalchemy.orm import Session
from sqlalchemy import or_
from sql_app import models, schemas


class AuthorRepo:
    async def create(db: Session, author: schemas.Author):
        db_author = models.Author(name=author.name, picture=author.picture)
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author

    def fetch_by_id(db: Session, _id):
        return db.query(models.Author).filter(models.Author.id == _id).first()

    def fetch_by_name(db: Session, name):
        return db.query(models.Author).filter(models.Author.name.contains(name)).first()

    def search_by_name(db: Session, name):
        return db.query(models.Author).filter(models.Author.name.like('%' + name + '%')).all()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Author).offset(skip).limit(limit).all()

    async def delete(db: Session, _id: int):
        db_author = db.query(models.Author).filter_by(id=_id).first()
        db.delete(db_author)
        db.commit()

    async def update(db: Session, author_data):
        updated_author = db.merge(author_data)
        db.commit()
        return updated_author


