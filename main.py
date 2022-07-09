
from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import RedirectResponse, JSONResponse
from typing import List, Optional
import uvicorn
from sql_app.author_repo import AuthorRepo
from sql_app import schemas as schemas
import db as db
from sql_app import models as models
from db import Session, engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='Library', openapi_url='/openapi.json')


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f'Failed to execute: {request.method}: {request.url}'
    return JSONResponse(status_code=400, content={'message': f'{base_error_message}. Detail: {err}'})


@app.post('/authors', tags=['Author'], response_model=schemas.Author, status_code=201)
async def create_author(author_request: schemas.AuthorCreate, db: db.Session = Depends(get_db)):
    """Create a new author"""
    db_author = AuthorRepo.fetch_by_name(db, name=author_request.name)
    if db_author:
        raise HTTPException(status_code=400, detail='Author already exists!')

    return await AuthorRepo.create(db=db, author=author_request)


@app.get('/authors', tags=['Author'], response_model=List[schemas.Author])
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


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)