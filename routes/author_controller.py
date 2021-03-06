from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
from slowapi import Limiter
from slowapi.util import get_remote_address

from db import get_db, Session
from sql_app.repositories.author_repo import AuthorRepo
from sql_app import schemas
from security import access_admin

router = APIRouter()
limiter = Limiter(key_func=get_remote_address, default_limits=['1/minute'])


@router.post('/', tags=['Author'], response_model=schemas.Author, status_code=201)
@limiter.limit('5/minute')
async def create_author(request: Request, author_request: schemas.AuthorCreate, admin: str = Depends(access_admin),
                        db: Session = Depends(get_db)):
    """
    Create a new author
    """
    if admin:
        db_author = AuthorRepo.fetch_by_name(db, name=author_request.name)
        if db_author:
            raise HTTPException(status_code=400, detail='Author already exists!')

        return await AuthorRepo.create(db=db, author=author_request)


@router.get('/', tags=['Author'], response_model=List[schemas.Author])
@limiter.limit('5/minute')
def get_all_authors(request: Request, name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all authors from the database
    """
    if name:
        db_author = AuthorRepo.search_by_name(db, name)
        if not db_author:
            raise HTTPException(status_code=400, detail='Author not found!')
        return db_author
    else:
        return AuthorRepo.fetch_all(db)


@router.patch('/{id}', status_code=204)
@limiter.limit('5/minute')
async def update_author(request: Request, id: int, author_request: schemas.AuthorUpdate, db: Session = Depends(get_db),
                        admin: str = Depends(access_admin)):
    """
    Update author information
    """
    if admin:
        db_author = AuthorRepo.fetch_by_id(db, id)
        if db_author:
            update_author_encoded = jsonable_encoder(author_request)
            if update_author_encoded['name']:
                db_author.name = update_author_encoded['name']
            if update_author_encoded['picture']:
                db_author.picture = update_author_encoded['picture']

            return await AuthorRepo.update(db=db, author_data=db_author)

        raise HTTPException(status_code=400, detail='Author not found with the given ID')
