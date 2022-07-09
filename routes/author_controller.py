from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List

from db import get_db, Session
from sql_app.author_repo import AuthorRepo
from sql_app import schemas

router = APIRouter()


@router.post('/authors', tags=['Author'], response_model=schemas.Author, status_code=201)
async def create_author(author_request: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """
    Create a new author
    """
    db_author = AuthorRepo.fetch_by_name(db, name=author_request.name)
    if db_author:
        raise HTTPException(status_code=400, detail='Author already exists!')

    return await AuthorRepo.create(db=db, author=author_request)


@router.get('/authors', tags=['Author'], response_model=List[schemas.Author])
def get_all_authors(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all authors from the database
    """
    if name:
        authors = []
        db_author = AuthorRepo.fetch_by_name(db, name)
        authors.append(db_author)
        return authors
    else:
        return AuthorRepo.fetch_all(db)
