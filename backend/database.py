import os
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from dotenv import load_dotenv

load_dotenv()

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
URL = os.getenv('URL')
DATABASE_NAME = os.getenv('DATABASE_NAME')

DB = 'postgresql://{0}:{1}@{2}/{3}'.format(LOGIN, PASSWORD, URL, DATABASE_NAME)

engine = create_engine(DB)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_database)]