from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from db import Session, get_db
from security import access_admin
from sql_app import schemas
from sql_app.repositories.paper_repo import PaperRepo
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post('/', response_model=schemas.Paper, status_code=201)
async def create_paper(paper_request: schemas.PaperCreate, admin: str = Depends(access_admin),
                       db: Session = Depends(get_db)):
    """
    Create a new paper
    """
    if admin:
        db_paper = PaperRepo.fetch_by_title(db, title=paper_request.title)
        if db_paper and db_paper.author_id == paper_request.author_id:
            raise HTTPException(status_code=400, detail='This paper already exists!')
        return PaperRepo.create(db=db, paper=paper_request)


@router.get('/', tags=['Paper'], response_model=List[schemas.PaperRead])
async def get_all_papers(search: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all papers from the database
    """
    if search:
        papers = []
        db_paper = PaperRepo.search_by_summary_or_title(db, search)
        if not db_paper:
            raise HTTPException(status_code=400, detail='Paper not found!')
        return db_paper
    else:
        return PaperRepo.fetch_all(db)


@router.patch('/{id}', status_code=204)
async def update_paper(id: int, paper_request: schemas.PaperUpdate, db: Session = Depends(get_db),
                       admin: str = Depends(access_admin)):
    """
    Update paper information
    """
    if admin:
        db_paper = PaperRepo.fetch_by_id(db, id)
        if db_paper:
            update_author_encoded = jsonable_encoder(paper_request)
            if update_author_encoded['summary']:
                db_paper.summary = update_author_encoded['summary']
            if update_author_encoded['body']:
                db_paper.body = update_author_encoded['body']
            if update_author_encoded['category']:
                db_paper.category = update_author_encoded['category']
            if update_author_encoded['first_paragraph']:
                db_paper.first_paragraph = update_author_encoded['first_paragraph']
            if update_author_encoded['title']:
                db_paper.title = update_author_encoded['title']

            return await PaperRepo.update(db=db, paper_data=db_paper)

        raise HTTPException(status_code=400, detail='Paper not found with the given ID')
