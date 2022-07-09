from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str
    hash_password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int

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


class PaperBase(BaseModel):
    id: int
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
