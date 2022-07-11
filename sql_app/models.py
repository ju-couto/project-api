from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    type = Column(String, default='user')

    def __repr__(self):
        return f'{self.username}, {self.type}'


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    picture = Column(String)

    papers = relationship('Paper', back_populates='author')
    def __repr__(self):
        return f'Author {self.name}'


class Paper(Base):
    __tablename__ = 'paper'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('author.id', name='author_id'))
    category = Column(String)
    title = Column(String)
    summary = Column(String)
    first_paragraph = Column(String)
    body = Column(String)

    author = relationship('Author', back_populates='papers')

    def __repr__(self):
        return f'{self.title}, {self.author_id}'


