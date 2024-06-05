import models
from database import engine, SessionLocal
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_database)]
