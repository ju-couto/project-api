from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://postgres:mariajulia@localhost:5432/library')
Session = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
