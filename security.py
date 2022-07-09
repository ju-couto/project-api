from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from db import Session, get_db
from sql_app.user_repo import UserRepo

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')
# CONFIG
SECRET_KEY = '43DDC799099616CC04D43815AAD5694B0768F7C66F2D1F193C2017786E7D3FB5'
ALGORITHM = 'HS256'
EXPIRES_IN_MIN = 5


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict):
    data_copy = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MIN)

    data_copy.update({'exp': expiration})

    token_jwt = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def verify_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')


def logged_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    exception = HTTPException(status_code=401, detail='Invalid token!')
    try:
        username = verify_access_token(token)
    except JWTError:
        raise exception

    if not username:
        raise exception
    db_user = UserRepo.fetch_by_username(db, username=username)

    if not db_user:
        raise exception
    return db_user
