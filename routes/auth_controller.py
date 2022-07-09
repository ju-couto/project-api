from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from db import get_db, Session
from sql_app.user_repo import UserRepo
from sql_app import schemas
from security import get_password_hash, verify_password, create_access_token, logged_user

router = APIRouter()


@router.post('/sigup', response_model=schemas.User, status_code=201)
async def sign_up(user_request: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    db_user = UserRepo.fetch_by_username(db, username=user_request.username)
    if db_user:
        raise HTTPException(status_code=400, detail='This username already exists!')
    user_request.password = get_password_hash(user_request.password)
    return await UserRepo.create(db=db, user=user_request)


@router.post('/token')
def login(login_request: schemas.Login, db: Session = Depends(get_db)):
    """
    Get access token
   """
    user_db = UserRepo.fetch_by_username(db, username=login_request.username)

    if not user_db:
        raise HTTPException(status_code=400, detail='Incorrect username or password!')
    valid_password = verify_password(login_request.password, user_db.password)

    if not valid_password:
        raise HTTPException(status_code=400, detail='Incorrect username or password!')
    token = create_access_token({'sub': user_db.username})
    return {'user': user_db, 'access_token': token}


@router.get('/me')
def me(user: schemas.User = Depends(logged_user), db: Session = Depends(get_db)):
    return user


@router.get('/users', response_model=List[schemas.User])
def get_all_users(username: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all users from the database
    """
    if username:
        users = []
        db_user = UserRepo.fetch_by_username(db, username)
        users.append(db_user)
        return users
    else:
        return UserRepo.fetch_all(db)
