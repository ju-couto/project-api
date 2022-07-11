from sqlalchemy.orm import Session
from sqlalchemy import or_
from sql_app import models, schemas


class PaperRepo:
    def create(db: Session, paper: schemas.Paper):
        db_paper = models.Paper(title=paper.title, summary=paper.summary, first_paragraph=paper.first_paragraph,
                                body=paper.body, author_id=paper.author_id, category=paper.category)
        db.add(db_paper)
        db.commit()
        db.refresh(db_paper)
        return db_paper

    def fetch_by_title(db: Session, title):
        return db.query(models.Paper).filter(models.Paper.title == title).first()

    def fetch_by_id(db: Session, _id):
        return db.query(models.Paper).filter(models.Paper.id == _id).first()

    def search_by_summary_or_title(db: Session, search):
        return db.query(models.Paper).filter(
            or_(models.Paper.summary.like('%' + search + '%'), models.Paper.title.like('%' + search + '%'))).all()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Paper).offset(skip).limit(limit).all()

    async def update(db: Session, paper_data):
        updated_author = db.merge(paper_data)
        db.commit()
        return updated_author
