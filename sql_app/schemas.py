from pydantic import BaseModel
from typing import Optional, List


class UserBase(BaseModel):
    id: int
    username: str
    password: str
    type: Optional[str]


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    id: int
    name: str
    picture: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class AuthorUpdate (BaseModel):
    name: Optional[str]
    picture: Optional[str]


class PaperBase(BaseModel):
    id: int
    author_id: int
    title: str
    category: str
    summary: str
    first_paragraph: str
    body: str


class PaperCreate(PaperBase):
    pass


class Paper(PaperBase):
    id: int

    class Config:
        orm_mode = True


class PaperRead(BaseModel):
    id: int
    author: Optional[Author]
    title: str
    category: str
    summary: str
    first_paragraph: str
    body: str


class Login(BaseModel):
    username: str
    password: str


class UserData(BaseModel):
    username: str


class SuccessLogin(BaseModel):
    user: str
    access_token: str

