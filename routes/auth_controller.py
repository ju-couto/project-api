from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from db import get_db, Session
from sql_app.user_repo import UserRepo
from sql_app import schemas
from security import get_password_hash, verify_password, create_access_token, logged_user, access_admin

router = APIRouter()


@router.post('/users', response_model=schemas.User, status_code=201)
async def sign_up(user_request: schemas.UserCreate, admin: str = Depends(access_admin), db: Session = Depends(get_db)):
    """
    Create a new user
    """
    if admin:
        db_user = UserRepo.fetch_by_username(db, username=user_request.username)
        if db_user:
            raise HTTPException(status_code=400, detail='This username already exists!')
        user_request.password = get_password_hash(user_request.password)
        return await UserRepo.create(db=db, user=user_request)


@router.post('/login', response_model=schemas.SuccessLogin)
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
    token = create_access_token({'user': user_db.username, 'type': user_db.type})
    return schemas.SuccessLogin(user=user_db.username, access_token=token)


@router.get('/me')
def me(user: schemas.User = Depends(logged_user)):
    return user


@router.get('/users', response_model=List[schemas.User])
def get_all_users(admin: str = Depends(access_admin), username: Optional[str] = None,
                  db: Session = Depends(get_db)):
    """
    Get all users from the database
    """
    if admin:
        if username:
            users = []
            db_user = UserRepo.fetch_by_username(db, username)
            users.append(db_user)
            return users
        else:
            return UserRepo.fetch_all(db)
