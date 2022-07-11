from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from fastapi.encoders import jsonable_encoder

from db import get_db, Session
from sql_app.repositories.author_repo import AuthorRepo
from sql_app import schemas
from security import access_admin

router = APIRouter()


@router.post('/', tags=['Author'], response_model=schemas.Author, status_code=201)
async def create_author(author_request: schemas.AuthorCreate, admin: str = Depends(access_admin),
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
def get_all_authors(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all authors from the database
    """
    if name:
        authors = []
        db_author = AuthorRepo.fetch_by_name(db, name)
        if not db_author:
            raise HTTPException(status_code=400, detail='Author not found!')
        authors.append(db_author)
        return authors
    else:
        return AuthorRepo.fetch_all(db)


@router.patch('/{id}', status_code=204)
async def update_author(id: int, author_request: schemas.AuthorUpdate, db: Session = Depends(get_db),
                        admin: str = Depends(access_admin)):
    """
    Update author information.
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
