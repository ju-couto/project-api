from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    id: Optional[int] = None
    name: str
    picture: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class PaperBase(BaseModel):
    id: Optional[int] = None
    author: Author
    title: str
    summary: str
    firstParagraph: str
    body: str


class PaperCreate(PaperBase):
    pass


class Paper(PaperBase):
    id: int

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class UserData(BaseModel):
    username: str


class SuccessLogin(BaseModel):
    user: str
    access_token: str

