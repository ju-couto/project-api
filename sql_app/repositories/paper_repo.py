from sqlalchemy.orm import Session

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
        return db.query(models.Paper).filter(models.Paper.title.contains(title)).first()

    def fetch_by_summary(db: Session, summary):
        return db.query(models.Paper).filter(models.Paper.summary.contains(summary)).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Paper).offset(skip).limit(limit).all()
