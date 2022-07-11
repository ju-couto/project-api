from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from db import Session, get_db
from security import access_admin
from sql_app import schemas
from sql_app.repositories.paper_repo import PaperRepo

router = APIRouter()


@router.post('/', response_model=schemas.Paper, status_code=201)
async def create_paper(paper_request: schemas.PaperCreate, admin: str = Depends(access_admin), db: Session = Depends(get_db)):
    """
    Create a new paper
    """
    if admin:
        db_paper = PaperRepo.fetch_by_title(db, title=paper_request.title)
        if db_paper and db_paper.author_id == paper_request.author_id:
            raise HTTPException(status_code=400, detail='This paper already exists!')
        return PaperRepo.create(db=db, paper=paper_request)


@router.get('/', tags=['Paper'], response_model=List[schemas.Paper])
async def get_all_papers(search_str: Optional[str] = None, db: Session =  Depends(get_db)):
    """
    Get all papers from the database
    """
    if search_str:
        papers = []
        db_paper_by_title = PaperRepo.fetch_by_title(db, search_str)
        db_paper_by_summary = PaperRepo.fetch_by_summary(db, search_str)
        if not db_paper_by_summary and not db_paper_by_title:
            raise HTTPException(status_code=400, detail='Paper not found!')
        papers.append(db_paper_by_summary or db_paper_by_title)
        return papers
    else:
        return PaperRepo.fetch_all(db)
