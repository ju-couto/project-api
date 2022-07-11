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


class Login(BaseModel):
    username: str
    password: str


class UserData(BaseModel):
    username: str


class SuccessLogin(BaseModel):
    user: str
    access_token: str


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
    id: Optional[int] = None
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


class PaperReadBase(BaseModel):
    id: Optional[int] = None
    author: Optional[Author]
    title: str
    category: str
    summary: str
    first_paragraph: str
    body: str


class PaperRead(PaperReadBase):
    id: int

    class Config:
        orm_mode = True


class PaperUpdate (BaseModel):
    title: Optional[str]
    category: Optional[str]
    summary: Optional[str]
    first_paragraph: Optional[str]
    body: Optional[str]

